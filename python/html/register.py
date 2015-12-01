#!/usr/bin/python

import mysql  #file i wrote
import kcmail #file i wrote
import re, string
import random
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
        return "nothing"
    result = mysql.execute_mysql("SELECT * FROM users WHERE username = '%s'" % (user))
    if not user or result: #no username give, or username exists
        return "user"
    result = mysql.execute_mysql("SELECT * FROM users WHERE email = '%s'" % (email))
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or result:
        return "email"
    if not passw or (passw != passw2) or (len(passw) < 8):
       return "password"

    pw_hash = pbkdf2_sha256.encrypt(passw, rounds=200000, salt_size=16)
    random.seed(passw)
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    mysql.execute_mysql( """INSERT INTO users (username, password, email, verified)
                          VALUES ('%s', '%s', '%s', '%s');"""
                          % (user, pw_hash, email, key) )
    kcmail.email_new_account(email, user, "http://keycellar.drago.ninja/register.cgi?verify=%s" % (key))
    return "ok"

#PRINT REGISTRATION FORM
def print_registration_form():
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print_html_file("register.html")

def print_verification_success():
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print_html_file("verified.html")

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("username", "")
email = form.getvalue("email", "")
password = form.getvalue("password", "")
password2 = form.getvalue("password2", "")
verify = form.getvalue("verify", "")

#DO STUFF WITH VARS
#PRINT STUFF TO GET VARS
r_result = register_user(username, email, password, password2)

if verify:
    mysql.execute_mysql("UPDATE users SET verified = '0' WHERE verified = '%s';" % (verify))
    print_verification_success()
if r_result == "ok":
    print "Location: http://keycellar.drago.ninja/u/faroeson"

if not verify:
    print_registration_form()

if r_result == "email":
    print "Invalid email address."
if r_result == "password":
    print "Password mismatch or under 8 characters."
elif r_result == "user":
    print "Invalid username or username taken."
