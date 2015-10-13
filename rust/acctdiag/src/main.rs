extern crate lib_andre;

use lib_andre::os::is_valid_user;
use std::error::Error;
use std::env;


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

    //check the first argument. if it's not a user, print usage > exit.
    let user = args[1].clone();

    println!("-- Checking user ...");
    if is_valid_user(user.as_ref()) {
        println!("-- {} is a valid user.", user);
    } else {
        println!("-- {} is an INVALID user.", user);
    }

    //now grabs the rest of the arguments.
    if args.contains(&"-i".to_string()) {
        argument_flags.interactive = true;
        println!("-- INTERACTIVE flag set.");
    }

//    for argument in args.clone() {
//        match argument.as_ref() {
//            "-i" => println!("-- INTERACTIVE flag set."),
//            _ => ,
//        }
//    }


    Ok(())
}





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
