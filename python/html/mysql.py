#!/usr/bin/python
import MySQLdb
import toml

def execute_mysql(query, args_tup):
    with open("db.toml") as toml_file:
        config = toml.loads(toml_file.read())
    db = MySQLdb.connect(host   ="localhost",
                         user   =config['database']['username'],
                         passwd =config['database']['password'],
                         db     =config['database']['database'])
    
    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor() 
    
    # Use all the SQL you like
    cur.execute(query, args_tup)
    
    #return the results
    return cur.fetchall()
