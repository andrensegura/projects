extern crate lib_andre;

use std::io;
use lib_andre::io::prompt;

fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), io::Error> {
    let name = try!(prompt("Name: "));
    let age = try!(prompt("Age: "));
    let username =  try!(prompt("Reddit Username: "));

    println!("\n\
        Your name: {}\n\
        Your age: {}\n\
        Your Reddit username: {} \n\
        ", name.trim(), age.trim(), username.trim());

    Ok(())
}
