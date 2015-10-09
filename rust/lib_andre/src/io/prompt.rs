//Prints the argument to the screen like a prompt and waits
//for the users input, then saves it to a string and returns it.

use std::io::prelude::*;
use std::io;

pub fn prompt(ps: &str) -> Result<String, io::Error> {
    let mut result = String::new();
    print!("{}", ps);
    try!(io::stdout().flush());
    try!(io::stdin().read_line(&mut result));
    Ok(result)
}
