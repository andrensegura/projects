#!/usr/bin/python

import mysql  #file i wrote
import kcmail #file i wrote
from functions import print_header, print_html_file, create_password_hash
import re, string
import random
import cgi
import cgitb; cgitb.enable() #for troubleshooting

#CHECKS REGISTRATION INPUT CRED, RETURNS ok ON SUCCESS
def register_user(user, email, passw, passw2):
    if not (user or email or passw or passw2):
        return "nothing"
    result = mysql.execute_mysql("""SELECT * FROM users WHERE username = %s""" , (user,))
    if not user or result: #no username give, or username exists
        return "user"
    result = mysql.execute_mysql("""SELECT * FROM users WHERE email = %s""" , (email,))
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or result:
        return "email"
    if not passw or (passw != passw2) or (len(passw) < 8):
       return "password"

    pw_hash = create_password_hash(passw)
    random.seed(passw)
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    mysql.execute_mysql( """INSERT INTO users (username, password, email, verified)
                          VALUES (%s, %s, %s, %s);"""
                          , (user, pw_hash, email, key,) )
    kcmail.email_new_account(email, user, "http://keycellar.com/register.cgi?verify=%s" % (key))
    return "ok"

def recover_password(action):
    if action == "1":
        rec_email = form.getvalue("rec_email", "")
        result = mysql.execute_mysql("""SELECT email FROM users WHERE email=%s;""", (rec_email,) )
        if not rec_email or not result:
            print "Not a valid email address."
        else:
            key = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                    string.digits) for _ in range(16))
            mysql.execute_mysql("""UPDATE users SET verified = %s WHERE email = %s;""" , (key, rec_email,))
            kcmail.email_password_recovery(rec_email, "https://keycellar.com/login?reset=%s" % (key))
            print """Password recovery email sent."""
            return 0
    print """<h3>Password Recovery:</h3>
            <form method="post" action="/register?recover=1">
            Email address: <input type="text" name="rec_email">
            <input type="submit" value="Send">
            <form>
          """

#PRINT REGISTRATION FORM
def print_registration_form():
    print_html_file("register.html")

def print_registration_success():
    print_html_file("success.html")
def print_verification_success():
    print_html_file("verified.html")

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("username", "")
email = form.getvalue("email", "")
password = form.getvalue("password", "")
password2 = form.getvalue("password2", "")
verify = form.getvalue("verify", "")
recover = form.getvalue("recover", "")

#DO STUFF WITH VARS
#PRINT STUFF TO GET VARS
r_result = register_user(username, email, password, password2)

print_header()


if recover:
    recover_password(recover)
elif verify:
    mysql.execute_mysql("""UPDATE users SET verified = '0' WHERE verified = %s;""" , (verify,))
    print_verification_success()
else:
    if r_result == "ok":
        print_registration_success()
    elif not verify:
        print_registration_form()

    if r_result == "email":
        print "Invalid email address."
    if r_result == "password":
        print "Password mismatch or under 8 characters."
    if r_result == "user":
        print "Invalid username or username taken."
