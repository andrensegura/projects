use std::io::prelude::*;
use std::fs::File;
use std::error::Error;

fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>>{
    println!("Content-type: text/html; charset=iso-8859-1\n");

    //header stuff
    try!(print_file("/home/andre/domains/drago.ninja/header.html"));

    //body stuff
    try!(print_file("body.html"));

    Ok(())
}

fn print_file(file_name: &str) -> Result<String, Box<Error>> {
    let mut f = try!(File::open(file_name));
    let mut s = String::new();
    try!(f.read_to_string(&mut s));
    println!("{}", s);

    Ok(s)
}
