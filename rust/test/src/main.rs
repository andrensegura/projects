use std::process::Command;
use std::env;

fn main() { 
    let args: Vec<_> = env::args().collect();
    let user = args[1].clone();

    println!("-- Checking user ...");
    
    if is_valid_user(user.as_ref()) {
        println!("-- User is valid: {}", user);
    } else {
        println!("-- User in invalid: {}", user);
    }
}

fn is_valid_user(user: &str) -> bool {
    let command = format!("{}{}", "id -u ", user);
    let output = Command::new("sh")
                            .arg("-c")
                            .arg(command)
                            .output()
                            .unwrap_or_else(|e| { panic!("failed to execute process: {}", e) }); 
    let output_str = String::from_utf8_lossy(&output.stdout);

    if output_str.is_empty() {
        false 
    } else {
        true
    }
}
