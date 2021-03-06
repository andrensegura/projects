extern crate regex;
extern crate curl;

use regex::Regex;
use curl::http;
use std::error::Error;
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
    let query_opts = try!(get_query_string());

    if query_opts.len() == 1{
        try!(print_file("body.html"));
    } else {
        let format = query_opts[0].split("=").last().unwrap().to_string();
        let advanced = query_opts[1].split("=").last().unwrap().to_string();
        let query_string = query_opts[2].split("=").last().unwrap().to_string();

        if query_string == "" {
            try!(print_file("body.html"));
            return Ok(());
        }


        try!(print_file("body.html"));
        println!("<div class=\"content\">List:<br>");

        //this line makes it autohighlight all
        //println!("<textarea type=\"text\" cols=\"50\" rows=\"10\" onclick=\"this.select()\">");
        println!("<form><textarea type=\"text\" name=\"result\" cols=\"50\" rows=\"10\">");

        let split = query_string.split("%0D%0A");

        let mut list_vec: Vec<String> = Vec::new();
        for s in split {
            list_vec.push(print_friendly(s, &format));
        }

        list_vec.sort();
        for item  in &list_vec {
            println!("{}", item);
        }

        println!("</textarea>");
        println!("<br><input type=\"button\" value=\"Select All\"");
        println!("onclick=\"javascript:this.form.result.focus();this.form.result.select();\">");
        println!("</form></div>");

    }

    Ok(())
}

fn print_friendly(line: &str, format: &String) -> String{
    let mut line = line.to_string();

    //replace %3A with colon.
    let mut re = Regex::new(r"%3A").unwrap();
    let mut result = re.replace_all(line.as_ref(), ":");

    //replace %26 with ampersand.
    re = Regex::new(r"%26").unwrap();
    result = re.replace_all(result.as_ref(), "&");

    //replace %27 with apostrophe.
    re = Regex::new(r"%27").unwrap();
    result = re.replace_all(result.as_ref(), "'");
    line = re.replace_all(line.as_ref(), "'"); //doing this so i can replace them later for correct searching

    //replace all remaining percent codes with nothing in
    //in the result string and the original.
    re = Regex::new(r"%[0-9A-F][0-9A-F]").unwrap();
    result = re.replace_all(result.as_ref(), "");
    //do it separately for line, as it will be used as a steam query.
    line = re.replace_all(line.as_ref(), "");
    re = Regex::new(r"'").unwrap();
    line = re.replace_all(line.as_ref(), "%27");

    //replace +'s with a space for the result.
    let re = Regex::new(r"\+").unwrap();
    result = re.replace_all(result.as_ref(), " ");

    line = get_app_url(line).unwrap();

    match format.as_ref() {
        "reddit"  => format!("* [{}]({})", result, line),
        "html"    => format!("<li><a href=\"{}\">{}</a><br>", line, result),
        _         => "something went wrong".to_string(),
    }
}

fn get_app_url(steam_query: String) -> Result<String, Box<Error>>{
    let url = format!("http://store.steampowered.com/search/?snr=&term={}", steam_query);

    let resp = http::handle().get(url).exec().unwrap();
    let body = std::str::from_utf8(resp.get_body()).unwrap();

    let re = Regex::new(r"http://store.steampowered.com/app/[0-9]*/").unwrap();
    let results = re.captures_iter(body).collect::<Vec<_>>();
    let steam_url = if results.len() == 0 {
                        "App not found :(".to_string()
                    }else{
                        results[0].at(0).unwrap().to_string()
                    };

    Ok(steam_url)

}

fn get_query_string() -> Result<Vec<String>, Box<Error>> {
    let key = "QUERY_STRING";
    let query = match env::var(key) {
                    Ok(val) => val,
                    Err(e) => e.to_string(),
                };

    let mut values: Vec<String> = Vec::new();
    for option in query.split("&") {
        values.push(option.to_string());
    }
    if values.len() == 2 {
        values.insert(1, "advanced=false".to_string());
    }
    
    Ok(values)

}
