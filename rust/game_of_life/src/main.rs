use std::error::Error;
use std::io::prelude::*;
use std::fs::File;
use std::char;

fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>> {
    const COLS: u32 = 11;
    const ROWS: u32 = 5;

    //its only ten long, but add 1 for the newline
    //should make it without newlines and just print them later.
    let mut grid = [[' '; COLS as usize]; ROWS as usize];          //how to make multi d array

    //get grid seed
    let file =  try!(get_file_contents("seed.txt".to_string()));

    //initialize the grid with the seed
    for i in 0..grid.len(){
        for j in 0..grid[0].len(){
            grid[i][j] = char::from_u32( file.as_bytes()[(i * COLS as usize) + j] as u32 ).unwrap();
        }
    }

    //print the grid's content
    for i in 0..grid.len() {
        for j in 0..grid[0].len(){
            print!("{}", grid[i][j]);
        }
    }

    //print the grid itself, then prints the file as bytes.
    println!("{:?}\n{:?}", grid, file.as_bytes());
    Ok(())
}


fn get_file_contents(f: String) -> Result<String, Box<Error>> {
    let mut f = try!(File::open(f));
    let mut result = String::new();
    try!(f.read_to_string(&mut result));

    Ok(result)
}
