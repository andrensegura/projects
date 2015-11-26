#!/usr/bin/python

import mysql
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256

#PRINTS OUT A FILE
def print_html_file(file_name):
    with open(file_name, 'r') as fin:
        print fin.read()

#CHECKS LOG IN CRED, RETURNS TRUE ON SUCCESS
def login(user, passw):
    if not (user and passw):
        return False
    result = mysql.execute_mysql("SELECT * FROM users WHERE username = '%s'" % (user))
    if not result:
        return False
    return pbkdf2_sha256.verify(passw, result[0][1])

#PRINT LOGIN FORM
def print_login_form():
    print "Content-type: text/html\n"
    print_html_file("/home/andre/domains/drago.ninja/header.html")
    print_html_file("login.html")
    if username or password:
        print "Invalid username or password."

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("username", "")
password = form.getvalue("password", "")

#DO STUFF WITH VARS
#PRINT STUFF TO GET VARS
if login(username, password):
    result = mysql.execute_mysql("SELECT * FROM users WHERE username = '%s'" % (username))
    if result[0][6] != "0":
        print "Location: http://keycellar.drago.ninja/success.html"
    else:
        print "Location: http://keycellar.drago.ninja/index.cgi"
print_login_form()

