extern crate lib_andre;

use lib_andre::io;

fn main() {
    let name = io::prompt("Name: ").unwrap();
    println!("Your name is {}.", name.trim());
    
    io::print_file("./test.txt").unwrap();
}
