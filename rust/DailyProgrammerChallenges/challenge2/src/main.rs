use std::error::Error;
use std::io::prelude::*;
use std::io;

fn main() {
    //calculator to calculate MPG, Miles, or Gallons based on any two
    //operands given
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>> {
    let choice = try!(prompt("Calculate MPG, Miles, or Gallons? (mpg/m/g): "));
 
    match choice.as_ref() {
        "mpg" => { println!("Calulating MPG.");
                   println!("Miles Per Gallon: {}", try!(calculate_mpg())); },
        "m" => { println!("Calulating possible distance.");
                   println!("Miles: {}", try!(calculate_miles())); },
        "g" => { println!("Calulating gallons needed.");
                   println!("Gallons: {}", try!(calculate_gallons())); },
        _ => println!("insufficient choice"),
    };

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

fn calculate_mpg() -> Result<f32, Box<Error>> {
    let miles_string = try!(prompt("Miles traveled: "));
    let gallons_string = try!(prompt("Gallons used: "));

    let miles_float = try!(miles_string.parse::<f32>());
    let gallons_float = try!(gallons_string.parse::<f32>());

    let mpg = miles_float / gallons_float;


    Ok(mpg)
}

fn calculate_miles() -> Result<f32, Box<Error>> {
    let gallons_string = try!(prompt("Gallons using: "));
    let mpg_string = try!(prompt("MPG of vehicle: "));

    let gallons_float = try!(gallons_string.parse::<f32>());
    let mpg_float = try!(mpg_string.parse::<f32>());

    let miles = mpg_float * gallons_float;


    Ok(miles)
}

fn calculate_gallons() -> Result<f32, Box<Error>> {
    let miles_string = try!(prompt("Miles traveled: "));
    let mpg_string = try!(prompt("MPG of vehicle: "));

    let miles_float = try!(miles_string.parse::<f32>());
    let mpg_float = try!(mpg_string.parse::<f32>());

    let gallons = miles_float / mpg_float;


    Ok(gallons)
}
