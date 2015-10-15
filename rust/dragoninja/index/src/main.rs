extern crate lib_andre;

use lib_andre::io::print_file;
use std::error::Error;

fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>>{
    println!("Content-type: text/html; charset=iso-8859-1\n");

    //header stuff
    println!("{}",try!(print_file("/home/andre/domains/drago.ninja/header.html")));

    //body stuff
    println!("{}", try!(print_file("body.html")));

    Ok(())
}
