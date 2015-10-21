extern crate lib_andre;
extern crate walkdir;

use walkdir::WalkDir;
use lib_andre::os::is_valid_user;
use lib_andre::io::{print_file, prompt};
//use std::process::Command;
use std::error::Error;
use std::env;
use std::os::unix::fs::PermissionsExt;
use std::path::{PathBuf, Path};
use std::fs::{metadata, File};
use std::io::Write;


struct Flags {
    interactive: bool,
    permissions: bool,
    suspended: bool,
    htaccess: bool,
    inodes: bool,

}


fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>> {

    let args: Vec<_> = env::args().collect();
    let mut argument_flags = Flags { interactive: false,
                                     permissions: false,
                                     suspended: false,
                                     htaccess: false,
                                     inodes: false };

    //no args
    if args.len() < 2 {
        print_usage();
        return Ok(())
    }

    //check the first argument. if it's not a user, print usage then exit.
    let user = args[1].clone();

    println!("-- Checking user ...");
    if is_valid_user(user.as_ref()) {
        println!("-- {} is a valid user.", user);
    } else {
        println!("-- {} is an INVALID user.", user);
        return Ok(())
    }

    //check args and run their functions if given.
    if args.contains(&"-i".to_string()) {
        argument_flags.interactive = true;
        println!("-- INTERACTIVE flag set.");
    }
    if args.contains(&"-s".to_string()) {
        argument_flags.suspended = true;
        try!(check_suspension(user.as_ref(), argument_flags.interactive));
    }
    if args.contains(&"-n".to_string()) {
        argument_flags.inodes = true;
        try!(check_inodes(user.as_ref(), argument_flags.interactive));
    }
    if args.contains(&"-p".to_string()) {
        argument_flags.permissions = true;
        try!(check_file_permissions(user.as_ref(), argument_flags.interactive));
    }
    if args.contains(&"-h".to_string()) {
        argument_flags.htaccess = true;
        try!(check_htaccess_files(user.as_ref(), argument_flags.interactive));
    }

    //user given, but no function arguments.
    //I originally wrote an if statement inside of this one to check the interactive
    //flag so it would decide wether to run this with/without interactive, but both
    //the with and without blocks ended up looking the same. Duh.
    if !(  argument_flags.suspended 
         | argument_flags.inodes 
         | argument_flags.permissions
         | argument_flags.htaccess ) {
        //no functions, but interactive. run all with interactive
        try!(check_suspension(user.as_ref(), argument_flags.interactive));
        try!(check_inodes(user.as_ref(), argument_flags.interactive));
        try!(check_file_permissions(user.as_ref(), argument_flags.interactive));
        try!(check_htaccess_files(user.as_ref(), argument_flags.interactive));
    }


    Ok(())
}



fn check_file_permissions(user: &str, interactive: bool) -> Result<(), Box<Error>>{
    println!("-- PERMISSIONS flag set. user:{} inter:{}", user, interactive);

    let mut homedir = PathBuf::from("/home/");
    homedir.push(user);

    let mut perms_vec = Vec::<(u32, String)>::new(); 

    for entry in WalkDir::new(&homedir) {
        let entry = match entry {
            Ok(v) => v,
            Err(_) => {continue;},
        };
        let meta = try!(metadata(entry.path()));
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
        println!("No results found.");
    } else {
        if interactive {
            let response: Vec<char> = try!(prompt("    Save results to a file?: "))
                                                .chars()
                                                .collect();
            if response[0].to_lowercase().next().unwrap() == 'y' {
                try!(save_to_file(homedir, user, ".perms.txt", perms_vec));
            }else{
                println!("Total files found: {}", perms_vec.len());
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
            println!("Total files found: {}", perms_vec.len());
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


fn check_suspension(user: &str, interactive: bool) -> Result<(), Box<Error>>{
    println!("-- SUSPENSION flag set. user:{} inter:{}", user, interactive);

    let mut suspend_file_path = PathBuf::from("/var/cpanel/suspended/");
    suspend_file_path.push(user);

    match print_file(suspend_file_path.to_str().unwrap()) {
        Ok(s) => println!("    {} is suspended: {}", user, s),
        Err(_) => println!("    {} is not suspended.", user),
    }


    Ok(())
}

fn check_htaccess_files(user: &str, interactive: bool) -> Result<(), Box<Error>>{
    println!("-- HTACCESS flag set. user:{} inter:{}", user, interactive);
    Ok(())
}

fn check_inodes(user: &str, interactive: bool) -> Result<(), Box<Error>>{
    println!("-- INODES flag set. user:{} inter:{}", user, interactive);

    let mut homedir = PathBuf::from("/home/");
    homedir.push(user);

    //not interactive, just give inodes.
    if !interactive {
        println!("    {} -- {}", try!(count_files(&homedir.as_path())), homedir.display());
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
                let entry = entry.unwrap();
                if try!(metadata(entry.path())).is_dir() {
                    results.push( (try!(count_files(entry.path())) ,
                                   entry.path().to_str().unwrap().to_string())  );
                }
            }
      
            if results.is_empty() {
                println!("No results found.");
            } else {
                results.sort();
                results.reverse();

                if response_file[0].to_lowercase().next().unwrap() != 'y' {
                    println!("Top 15 results:");
                    let mut count = 0;
                    for item in results {
                        count += 1;
                        println!("    {} -- {}", item.0, item.1);
                        if count >=15 { break; }
                    }
                } else {
                    let mut file_path = PathBuf::from(homedir.as_path());
                    file_path.push(user.to_string() + ".inodes.txt");
                    let mut file = try!(File::create(file_path.clone()));


                    //could just print with this, that way I could write a function
                    //that handles making the file, but the output is ugly:
                    //try!(write!(file, "{:?}", results));
                    //I could make a new variable and format it, then pass it to the
                    //supposed function, I guess. Hrm.
                    for item in results {
                        try!(write!(file, "{} -- {}\n", item.0, item.1));
                    }

                    //println!("    Saved to {:?}", file_path);
                }
            }
        //no breakdown. just print the inodes.
        } else {
            println!("    {} -- {}", try!(count_files(&homedir.as_path())), homedir.display());
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
Certified Hosting -- acctDiag -- Usage
This tool is used to diagnose common issues with cPanel users. The program will 
make no changes to accounts (unless using interactive mode, be careful!), but
will report issues that it finds.

This is still a work in progress. Issues may be found, features may be added.
Any bugs, issues, or feature requests can be sent to andre@certifiedhosting.com.

>>SYNTAX:
[~]# acctDiag CPUSER <-i> <-n> <-p> <-h> <-s>
*************
CPUSER          :       Must be a valid cPanel user. MUST BE FIRST ARGUMENT.
-i              :       INTERACTIVE flag. Setting this flag will allow you
                        make runtime decisions. Try it out. MUST BE 2nd ARG.
*************
-n              :       Check the amount of iNodes the account has.
-p              :       Check file/directory Permissions.
-h              :       Check for issues with a .Htaccess file.
-s              :       Check if the account is Suspended.
*************
CPUSER must come first, -i must come second (optional).
The rest may be in any order.
You do not need to include any flags. By default, the program will have all
flags set; setting one manually turns all others off.
-Andre
-------------------------------------------------------------------------------
"#;
    println!("{}", usage);
}
