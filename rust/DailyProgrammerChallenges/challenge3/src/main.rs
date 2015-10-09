use std::error::Error;
use std::io::prelude::*;
use std::io;
use std::env;
use std::fs::File;
use std::char;

fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>> {
    let args: Vec<_> = env::args().collect();
    let mut file: String;
    let mut decrypt = false;
    let mut result: String;

    //encrypt: default behavior. assuming there is no argument [arg.len()==1]
    if args.len() == 1 {
        file = try!(prompt("File to cipher: "));
    //decrypt: assuming there are more than one arg and the first is "-d"
    } else if args[1].to_string() == "-d" {
        //only arg is "-d"
        decrypt = true;
        if args.len() == 2 {
            file = try!(prompt("File to decrypt: "));
        //there is a file given
        } else {
            file = args[2].to_string();
        }
    //encrypt: one argument or more, get the first. encrypt   
    } else {
        file = args[1].to_string();
    }

    let input = try!(get_file_contents(file));

    if decrypt {
        result = try!(decipher(input.clone()));
    } else {
        result = try!(cipher(input.clone()));
    }
//    println!("{}", input);
    println!("{}", result.trim());

    Ok(())
}

fn prompt(ps: &str) -> Result<String, io::Error> {
    let mut response = String::new();
    print!("{}", ps);
    try!(io::stdout().flush());
    try!(io::stdin().read_line(&mut response));
    let trimmed_response = response.trim();
    Ok(trimmed_response.to_string())
}

fn get_file_contents(f: String) -> Result<String, Box<Error>> {
    let mut f = try!(File::open(f));
    let mut result = String::new();
    try!(f.read_to_string(&mut result));

    Ok(result)
}

fn cipher(original_text: String) -> Result<String, Box<Error>> {
    let mut result = String::new();
    let mut next_char: char;

    for c in original_text.chars() {
        if !(char::is_whitespace(c)) {
            next_char = char::from_u32((c as u32) + 1 ).unwrap();
        } else {
            next_char = c;
        }
        result.push(next_char);
    }

    Ok(result)
}

fn decipher(original_text: String) -> Result<String, Box<Error>> {
    let mut result = String::new();
    let mut next_char: char;

    for c in original_text.chars() {
        if !(char::is_whitespace(c)) {
            next_char = char::from_u32((c as u32) - 1 ).unwrap();
        } else {
            next_char = c;
        }
        result.push(next_char);
    }

    Ok(result)
}
