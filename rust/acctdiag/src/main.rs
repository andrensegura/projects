extern crate regex;
extern crate lib_andre;
extern crate walkdir;

use walkdir::WalkDir;
use lib_andre::os::is_valid_user;
use lib_andre::io::{print_file, prompt};
//use std::process::Command;
use std::error::Error;
use std::{env, thread};
use std::sync::Arc;
use std::os::unix::fs::PermissionsExt;
use std::path::{PathBuf, Path};
use std::fs::{metadata, File};
use std::io::prelude::*;
use regex::Regex;


const RED: &'static str = "\u{1B}[0;31m";
const GREEN: &'static str = "\u{1B}[0;32m";
const BLUE: &'static str = "\u{1B}[0;34m";
const NC: &'static str = "\u{1B}[0m";


fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>> {


    let args: Vec<_> = env::args().collect();

    let mut interactive: bool = false;
    let mut permissions: bool = false;
    let mut suspended:   bool = false;
    let mut htaccess:    bool = false;
    let mut inodes:      bool = false;

    //no args
    if args.len() < 2 {
        print_usage();
        return Ok(())
    }

    let mut children = vec![];

    println!("{}Account Diagnostics Tool v1.2.0 -- Andre Segura{}", BLUE, NC);

    //check the first argument. if it's not a user, print usage then exit.
    let user = Arc::new(args[1].clone());

    println!("-- {}Checking user{}...", BLUE, NC);
    if is_valid_user(user.as_ref()) {
        println!("    {} is a valid user.", user);
    } else {
        println!("    {} is an {}INVALID{} user.", user, RED, NC);
        return Ok(())
    }

    //check args and run their functions if given.
    if args.contains(&"-i".to_string()) {
        interactive = true;
        println!("-- Flag '-i': Running in INTERACTIVE mode.");
    }
    if args.contains(&"-s".to_string()) {
        suspended = true;
        try!(check_suspension(user.as_ref()));
    }
    if args.contains(&"-n".to_string()) {
        inodes = true;
        let user = user.clone(); //increments the Arc counter.
        if interactive {
            try!(check_inodes(user.as_ref(), true));
        }else{
            children.push(thread::spawn(move || {
                check_inodes(user.as_ref(), false).unwrap();
            }));
        }
    }
    if args.contains(&"-p".to_string()) {
        permissions = true;
        let user = user.clone(); //increments the Arc counter.
        if interactive {
            try!(check_file_permissions(user.as_ref(), true));
        }else{
            children.push(thread::spawn(move || {
                check_file_permissions(user.as_ref(), false).unwrap();
            }));
        }
    }
    if args.contains(&"-h".to_string()) {
        htaccess = true;
        let user = user.clone(); //increments the Arc counter.
        if interactive {
            try!(check_htaccess_files(user.as_ref(), interactive));
        }else{
            children.push(thread::spawn(move || {
                check_htaccess_files(user.as_ref(), interactive).unwrap();
            }));
        }
    }

    //user given, but no function arguments.
    //I originally wrote an if statement inside of this one to check the interactive
    //flag so it would decide wether to run this with/without interactive, but both
    //the with and without blocks ended up looking the same. Duh.
    if !(  suspended 
         | inodes 
         | permissions
         | htaccess ) {
        try!(check_suspension(user.as_ref()));
        if interactive {
            try!(check_inodes(user.as_ref(), true));
            try!(check_file_permissions(user.as_ref(), true));
            try!(check_htaccess_files(user.as_ref(), interactive));
        }else{
            {   let user = user.clone(); //increments the Arc counter.
                children.push(thread::spawn(move || {
                    check_inodes(user.as_ref(), false).unwrap();
                }));
            }{  let user = user.clone(); //increments the Arc counter.
                children.push(thread::spawn(move || {
                    check_file_permissions(user.as_ref(), false).unwrap();
                }));
            }{  let user = user.clone(); //increments the Arc counter.
                children.push(thread::spawn(move || {
                    check_htaccess_files(user.as_ref(), interactive).unwrap();
                }));
            }
        }
    }

    for child in children {
        //wait for the thread to finish. returns a result.
        let _ = child.join();
    }

    Ok(())
}



fn check_file_permissions(user: &str, interactive: bool) -> Result<(), Box<Error>>{
    println!("-- {}Checking for excessive file permissions{}...", BLUE, NC);

    let mut homedir = PathBuf::from("/home/");
    homedir.push(user);

    let mut perms_vec = Vec::<(u32, String)>::new(); 

    for entry in WalkDir::new(&homedir) {
        //if there's a problem, just skip it.
        let entry = match entry {
            Ok(v) => v,
            Err(_) => {continue;},
        };
        let meta = match metadata(entry.path()){
            Ok(v) => v,
            Err(_) => {continue;},
        };
        let mode = meta.permissions().mode();

        //after lots of tinkering, i figured, duh, biwise and.
        //I was also going to test if the value came out to be 2, 16, or 18,
        //but duh, if it's over 0 then one of the flags are set.
        if (mode & 0b00010010u32) > 0 {
            //this was a bit ridiculous haha.
            //it formats mode, which is a u32, into its octal value as a string,
            //then we parse that string back into a u32. Is there no easier way
            //to just convert a u32 into an octal u32?
            perms_vec.push( ( format!("{:o}", mode).parse::<u32>().unwrap(),
                            entry.path().to_str().unwrap().to_string()) );
        }
    }

    perms_vec.sort();

    if perms_vec.is_empty() {
        println!("\n{}PERMISSIONS INFO{}:", GREEN, NC);
        println!("    No results found.");
    } else {
        if interactive {
            let response: Vec<char> = try!(prompt("    Save results to a file?: "))
                                                .chars()
                                                .collect();
            if response[0].to_lowercase().next().unwrap() == 'y' {
                try!(save_to_file(homedir, user, ".perms.txt", perms_vec));
                println!("    Saved to /home/{0}/{0}.perms.txt", user);
            }else{
                println!("    Total files found: {}", perms_vec.len());
                perms_vec.reverse();
                let mut count = 1;
                let mut last = 0;
                for item in perms_vec {
                    if item.0 == last {
                        count += 1;
                    }else{
                        if count != 1 {
                            println!("    Perms: {}\tAmt Files: {}", last, count);
                            count = 1;
                        }
                        last = item.0;
                    }
                }
                println!("    Perms: {}\tAmt Files: {}", last, count);
            }
        }else{
            println!("\n{}PERMISSIONS INFO{}:", GREEN, NC);
            println!("    Total files found: {}", perms_vec.len());
            perms_vec.reverse();
            let mut count = 1;
            let mut last = 0;
            //I feel like reading this block makes sense, but it took me a while
            //to get it just right. Should I add comments? ...hmm. Probably.
            for item in perms_vec {
                if item.0 == last {
                    count += 1;
                }else{
                    if count != 1 {
                        println!("    Perms: {}\tAmt Files: {}", last, count);
                        count = 1;
                    }
                    last = item.0;
                }
            }
            println!("    Perms: {}\tAmt Files: {}", last, count);
        }
    }

    Ok(())
}


fn check_suspension(user: &str) -> Result<(), Box<Error>>{
    println!("-- {}Checking suspension status{}...", BLUE, NC);

    let mut suspend_file_path = PathBuf::from("/var/cpanel/suspended/");
    suspend_file_path.push(user);

    //I love this. basically, why check if the file exists when you can just try
    //opening it? if you can't open it, then it doesn't exist! Much more elegant.
    match print_file(suspend_file_path.to_str().unwrap()) {
        Ok(s) => println!("    {} is {}suspended{}. Reason: {}", user, RED, NC, s),
        Err(_) => println!("    {} is not suspended.", user),
    }


    Ok(())
}

fn check_htaccess_files(user: &str, interactive: bool) -> Result<(), Box<Error>>{
    println!("-- {}Checking for suPHP .htaccess conflicts{}...", BLUE, NC);

    let mut homedir = PathBuf::from("/home/");
    homedir.push(user);

    let mut hta_vec = Vec::<(String)>::new(); 

    for entry in WalkDir::new(&homedir) {
        let entry = match entry {
            Ok(v) => v,
            Err(_) => {continue;},
        };
        if entry.path().file_name().unwrap() == ".htaccess" {
            let re = Regex::new("(?m)^(?P<val>(Options|php_(flag|value)|AddHandler)(.*))").unwrap();
            let mut f = try!(File::open(entry.path()));
            let mut buffer = String::new();
            try!(f.read_to_string(&mut buffer));
            if re.is_match(buffer.as_ref()) {
                hta_vec.push(format!("    -- {}", entry.path().display()));
                for cap in re.captures_iter(buffer.as_ref()).collect::<Vec<_>>(){
                    hta_vec.push(format!("      {}", cap.name("val").unwrap()));
                }
            }
        }
    }

    if !interactive { println!("\n{}HTACCESS INFO{}:", GREEN, NC); }

    if hta_vec.is_empty() {
        println!("    No results found.");
    } else {
        for item in hta_vec {
            println!("{}", item);
        }
    }

    Ok(())
}

fn check_inodes(user: &str, interactive: bool) -> Result<(), Box<Error>>{
    println!("-- {}Gathering inode information{}...", BLUE, NC);

    let mut homedir = PathBuf::from("/home/");
    homedir.push(user);

    let total_inodes = try!(count_files(&homedir.as_path()));

    //not interactive, just give inodes.
    if !interactive {
        println!("\n{}INODE INFORMATION{}:", GREEN, NC);
        if total_inodes >= 250000 {
            println!("    {}{}{} -- {}", RED, total_inodes, NC, homedir.display());
        } else {
            println!("    {} -- {}", total_inodes, homedir.display());
        }
    //interactive. what do you want to do?
    } else {
        //it's difficult to access the chars in a string, so we convert it to a Vec
        let response_breakdown: Vec<char> = try!(prompt("    See breakdown of inode usage?: "))
                                            .chars()
                                            .collect();
        //.to_lowercase returns an iterator that corresponds to the lower case equivalent.
        //calling .next() returns Some(char), so we unwrap it.
        //they want to see the breakdown.
        if response_breakdown[0].to_lowercase().next().unwrap() == 'y' {
            let response_file: Vec<char> = try!(prompt("    Save it to a file?: "))
                                           .chars()
                                           .collect();
            let mut results = Vec::<(u32, String)>::new();
            for entry in WalkDir::new(&homedir) {
                let entry = match entry {
                    Ok(v) => v,
                    Err(_) => {continue;},
                };
                if try!(metadata(entry.path())).is_dir() {
                    results.push( (try!(count_files(entry.path())) ,
                                   entry.path().to_str().unwrap().to_string())  );
                }
            }
      
            if results.is_empty() {
                println!("\n{}INODE INFORMATION{}:", GREEN, NC);
                println!("    No results found.");
            } else {
                results.sort();
                results.reverse();

                if response_file[0].to_lowercase().next().unwrap() != 'y' {
                    println!("    Top 15 results:");
                    let mut count = 0;
                    for item in results {
                        count += 1;
                        println!("    {} -- {}", item.0, item.1);
                        if count >=15 { break; }
                    }
                } else {
                    try!(save_to_file(homedir, user, ".inodes.txt", results));
                    println!("    Saved to /home/{0}/{0}.inodes.txt", user);
                }
            }
        //no breakdown. just print the inodes.
        } else {
            println!("\n{}INODE INFORMATION{}:", GREEN, NC);
            if total_inodes >= 250000 {
                println!("    {}{}{} -- {}", RED, total_inodes, NC, homedir.display());
            } else {
                println!("    {} -- {}", total_inodes, homedir.display());
            }
        }
    }

    Ok(())
}

fn count_files(dir: &Path) -> Result<u32, Box<Error>>{
    let mut count = 0;
    //you can discard the value by using "_"
    for _ in WalkDir::new(&dir) {
        count += 1;
    }
    Ok(count)
}

fn save_to_file(dir: PathBuf, username: &str, extension:
                &str, vec: Vec<(u32, String)>)-> Result<(), Box<Error>>{
    let mut file_path = PathBuf::from(dir.as_path());
    file_path.push(username.to_string() + extension);
    let mut file = try!(File::create(file_path.clone()));

    for item in vec {
        try!(write!(file, "{} -- {}\n", item.0, item.1));
    }

    Ok(())
}


//fn get_command_output(command: String) -> String {
//    let output = Command::new("sh")
//                            .arg("-c")
//                            .arg(command)
//                            .output()
//                            .unwrap_or_else(|e| { panic!("failed to execute process: {}", e) });
//    String::from_utf8_lossy(&output.stdout).to_string()
//}



fn print_usage() {
    let usage = r#"
-------------------------------------------------------------------------------
Certified Hosting -- acctdiag 1.2.0 -- Usage
This tool is used to diagnose common issues with cPanel users. The program will 
make no changes to accounts (interactive mode may in the future, be careful!),
but will report issues that it finds.

Threading support:
This program will run the more hard working functions in their own threads
(inodes/perms/htaccess) when *not* using interactive mode. This greatly reduces
runtime. Please report any issues (formatting or otherwise) that you encounter.

>>SYNTAX:
[~]# acctdiag CPUSER <-i> <-n> <-p> <-h> <-s>
*************
CPUSER          :       Must be a valid cPanel user. MUST BE FIRST ARGUMENT.
-i              :       INTERACTIVE flag. Setting this flag will allow you
                        make runtime decisions. Try it out.
*************
-n              :       Check the amount of iNodes the account has.
-p              :       Check file/directory Permissions.
-h              :       Check for issues with .Htaccess files.
-s              :       Check if the account is Suspended.
*************
Except for the username, the rest of the options may be in any order.
You do not need to include any flags. Running with no arguments would be the
same as running `acctdiag user -n -p -h -s`.

This is still a work in progress. Issues may be found, features may be added.
Any bugs, problems, or feature requests can be sent to andre@certifiedhosting.com.

-Andre
-------------------------------------------------------------------------------
"#;
    println!("{}", usage);
}
