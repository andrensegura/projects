#!/usr/bin/python

import mysql
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256

#PRINTS OUT A FILE
def print_html_file(file_name):
    with open(file_name, 'r') as fin:
        print fin.read()

#CHECKS REGISTRATION INPUT CRED, RETURNS ok ON SUCCESS
def register_user(user, email, passw, passw2):
    if not (user or email or passw or passw2):
        return "sad"
    result = mysql.execute_mysql("SELECT * FROM users WHERE username = '%s'" % (user))
    if not user or result: #no username give, or username exists
        return "user"
    if not passw or (passw != passw2) or (len(passw) < 8):
       return "password"
    return "ok"

#PRINT REGISTRATION FORM
def print_registration_form():
    print "Content-type: text/html\n"
    print_html_file("/home/andre/domains/drago.ninja/header.html")
    print_html_file("register.html")

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("username", "")
email = form.getvalue("email", "")
password = form.getvalue("password", "")
password2 = form.getvalue("password2", "")

#DO STUFF WITH VARS
#PRINT STUFF TO GET VARS
r_result = register_user(username, email, password, password2)
if r_result == "ok":
    print "Location: http://keycellar.drago.ninja/success.html"
print_registration_form()
if r_result == "password":
    print "Password mismatch or under 8 characters."
elif r_result == "user":
    print "Invalid username or username taken."
