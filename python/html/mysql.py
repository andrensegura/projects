#!/usr/bin/python
import MySQLdb
from config import DB_NAME, DB_USER, DB_PASS

def execute_mysql(query, args_tup):
    db = MySQLdb.connect(host   ="localhost",
                         user   =DB_USER,
                         passwd =DB_PASS,
                         db     =DB_NAME)
    
    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor() 
    
    # Use all the SQL you like
    cur.execute(query, args_tup)
    
    #return the results
    return cur.fetchall()
