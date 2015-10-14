use std::error::Error;
use std::path::PathBuf;
use std::fs::File;
use std::io::prelude::*;


fn main() {
    let user = "employee";
    
    let mut suspend_file_path = PathBuf::from("/var/cpanel/suspended/");
    suspend_file_path.push(user);
    
    match print_file(suspend_file_path.to_str().unwrap()) {
        //Ok(s) => println!("{} is SUSPENDED: {}", user, s),
        Ok(s) => println!("{} is SUSPENDED.", user),
        Err(_) => println!("{} is not suspended.", user),
    }
    
    

}


pub fn print_file(file_name: &str) -> Result<String, Box<Error>> {
    let mut f = try!(File::open(file_name));
    let mut s = String::new();
    try!(f.read_to_string(&mut s));

    Ok(s)
}

