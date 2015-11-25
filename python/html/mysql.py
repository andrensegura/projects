#!/usr/bin/python
import MySQLdb

def execute_mysql(query):
    db = MySQLdb.connect(host="localhost",      # your host, usually localhost
                         user="andre_kc",       # your username
                         passwd="7QS8R8cZ6azd", # your password
                         db="andre_kc")         # name of the data base
    
    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor() 
    
    # Use all the SQL you like
    cur.execute(query)
    
    #return the results
    return cur.fetchall()
