extern crate walkdir;
use walkdir::WalkDir;
use std::error::Error;
use std::path::PathBuf;
use std::path::Path;
use std::fs::metadata;

fn main() {
    try().unwrap();
}

fn try() -> Result<(), Box<Error>>{

    let mut results = Vec::<(String)>::new();
    //let mut results = Vec::<(walkdir::DirEntry)>::new();
    for entry in WalkDir::new("/home/employee") {
        let entry = entry.unwrap();
        let entry_meta = try!(metadata(entry.path()));
        if entry_meta.is_dir() {
            results.push(entry.path().to_str().unwrap().to_string());
        }
    }
    Ok(())
}
