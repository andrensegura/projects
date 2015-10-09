use std::error::Error;
use std::io::prelude::*;
use std::fs::File;

fn main() {

    try_main().unwrap();

}

fn try_main() -> Result<String, Box<Error>>{
    //let mut f = try!(File::create("foo.txt"));
    let mut f = try!(File::open("foo.txt"));
    let mut s = String::new();
    try!(f.read_to_string(&mut s));
    println!("{}", s);

    Ok(s)
}
