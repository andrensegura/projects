extern crate lib_andre;
extern crate toml;
extern crate mysql;

use lib_andre::io::print_file;
use std::error::Error;
use toml::Value;
use mysql::conn::MyOpts;
use mysql::conn::pool::MyPool;
use std::default::Default;

fn main() {
    try_main().unwrap();
}

fn try_main() -> Result<(), Box<Error>>{
    println!("Content-type: text/html; charset=iso-8859-1\n");

    //header stuff
    println!("{}",try!(print_file("/home/andre/domains/drago.ninja/header.html")));

    //body stuff
    println!("{}", try!(print_file("body.html")));

    //mysql test
    mysql_stuff();

    Ok(())
}


fn mysql_stuff() {
    println!("<h1>testing</h1>");
    let database_toml: toml::Value = print_file("db.toml").unwrap().parse().unwrap();

    let db = MyOpts {
        user:     Some(database_toml.lookup("database.username").unwrap()
                    .as_str().unwrap().to_string()),
        pass:     Some(database_toml.lookup("database.password").unwrap()
                    .as_str().unwrap().to_string()),
        db_name:  Some(database_toml.lookup("database.database").unwrap()
                    .as_str().unwrap().to_string()),
        //THIS CRATE DOESN'T ACCEPT LOCALHOST. WTF
        //THE BELOW JUST GETS DEFAULTED TO 127.0.0.1 IF IT'S NOT AN IP(v4|v6)
        tcp_addr: Some("localhost".to_string()),
        ..Default::default()
    };

//    println!("{}\n{}", db.db_name.unwrap(),
//        database_toml.lookup("database.username").unwrap().as_str().unwrap());

    let pool = MyPool::new(db).unwrap();
    for mut stmt in pool.prepare(r"show databases;").into_iter() {
        stmt.execute(()).unwrap();
    }


}
