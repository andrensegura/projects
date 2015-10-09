use std::fs;
use std::error::Error;
use std::process::Command;
use std::io::prelude::*;
use std::fs::File;
use std::env;

fn main() {

    try_main().unwrap();

}


fn try_main() -> Result<(), Box<Error>> {
    println!("Content-type: text/html; charset=iso-8859-1\n");

    //print header stuff
    try!(print_file("/home/andre/domains/drago.ninja/header.html"));

    //print body stuff
    println!("<body>");
    try!(print_body_content());
    println!("</body>");

    //print footer stuff
    try!(print_file("footer.html"));

    Ok(())

}

fn print_file(file_name: &str) -> Result<String, Box<Error>> {
    let mut f = try!(File::open(file_name));
    let mut s = String::new();
    try!(f.read_to_string(&mut s));
    println!("{}", s);

    Ok(s)
}

fn print_body_content() -> Result<(), Box<Error>>{
    let query_string = try!(get_query_string());

    if query_string == "" {
        try!(print_file("list.html"));
    } else {
        let file = query_string.clone() + ".html";
        let file_metadata = try!(fs::metadata(file.clone()));
        //check to see if the query is a valid file before checking the challenges
        if file_metadata.is_file() {
            try!(print_file(file.as_ref()));
        //now treat it like a challenge post
        }else if print_selector(try!(query_string.parse::<i32>())) {
            try!(print_file(file.as_ref())); 
        } else {
            try!(print_file("list.html"));
        }
    }

    Ok(())
}

fn print_selector(query: i32) -> bool {
    let output = Command::new("sh")
                          .arg("-c")
                          .arg("ls [0-9]* | cut -d'.' -f1 | tail -1")
                          .output()
                          .unwrap_or_else(|e| { panic!("failed to execute process: {}", e) });
    let latest = String::from_utf8_lossy(&output.stdout);

    //makes sure the query isn't out of bounds.
    //forgot to do this before.
    if query < 1 || query > latest.trim().parse::<i32>().unwrap() {
        return false;
    } else {
        if query != 1 {
            println!("<a href='http://drago.ninja/rust/1'><<</a>");
            println!("&emsp;");
            println!("<a href='http://drago.ninja/rust/{}'><</a>", query - 1 );
        }
        println!("&emsp;{}&emsp;", query);
        if query.to_string() != latest.trim() {  //lolol the latest variable has a newline.
            println!("<a href='http://drago.ninja/rust/{}'>></a>", query + 1 );
            println!("&emsp;");
            println!("<a href='http://drago.ninja/rust/{}'>>></a>", latest);
        }
    }
    true
}


fn get_query_string() -> Result<String, Box<Error>> {
    let key = "QUERY_STRING";
    let query = match env::var(key) {
                    Ok(val) => val,
                    Err(e) => e.to_string(),
                };

    Ok(query)
}
