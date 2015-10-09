//Prints the argument to the screen like a prompt and waits
//for the users input, then saves it to a string and returns it.

use std::io::prelude::*;
use std::fs::File;
use std::error::Error;
use std::io;

pub fn prompt(ps: &str) -> Result<String, io::Error> {
    let mut result = String::new();
    print!("{}", ps);
    try!(io::stdout().flush());
    try!(io::stdin().read_line(&mut result));
    Ok(result)
}

//take a file name as a string and prints the contents of the file
//if it exists.
pub fn print_file(file_name: &str) -> Result<String, Box<Error>> {
    let mut f = try!(File::open(file_name));
    let mut s = String::new();
    try!(f.read_to_string(&mut s));
    println!("{}", s);

    Ok(s)
}
