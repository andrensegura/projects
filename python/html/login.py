#!/usr/bin/python

import mysql, steam #files i wrote
import cgi, os, string
import Cookie, mycookie, datetime
import random
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256
from dbstructure import USERNAME, PASSWORD 

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
    return pbkdf2_sha256.verify(passw, result[0][PASSWORD])

def create_session(user, passw):
    expires = datetime.datetime.now() + datetime.timedelta(days=3) 
    cookie = Cookie.SimpleCookie()
    random.seed(passw)
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)) 
    cookie["session"] = key
    cookie["session"]["domain"] = ".keycellar.drago.ninja"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    #set key in database
    mysql.execute_mysql("UPDATE users SET logged_in = '%s' WHERE username = '%s';"
                        % (key, user) )
    return cookie

#PRINT LOGIN FORM
def print_login_form(user, passw):
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print_html_file("login.html")
    if user or passw:
        print "Invalid username or password."
def print_login_success(user):
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print_html_file("success.html")
    print """Proceed to your <a href="profile.cgi?user=%s">profile.</a>""" % (user)
def print_logout(user):
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print """<a href="login?action=logout">Logout(%s)</a>""" % (user)
def print_lo():
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print_html_file("logout.html")

def main():
    #GET VARIABLES
    form = cgi.FieldStorage()
    username = form.getvalue("username", "")
    password = form.getvalue("password", "")
    action = form.getvalue("action", "")

    #CHECK COOKIE
    session = mycookie.get_cookie()
    if session:
        result = mysql.execute_mysql("SELECT * FROM users WHERE logged_in = '%s'"
                   % (session["session"].value))
        username = result[0][USERNAME] if result else username

    #DO STUFF WITH VARS
    #PRINT STUFF TO GET VARS
    if action == "logout" and session:
        mysql.execute_mysql("UPDATE users SET logged_in = '0' WHERE logged_in = '%s';"
                            % (session["session"].value))
        session["session"] = ""
        print session
        print_lo()
    elif action == "update" and session:
        if login(username,password):
            up_email = form.getvalue("up_email", "")
            up_steam = form.getvalue("up_steam", "")
            if up_email:
                mysql.execute_mysql("UPDATE users SET email = '%s' WHERE username = '%s';"
                        % (up_email, username) )
            if up_steam:
                up_steam = steam.get_profile(up_steam)
                mysql.execute_mysql("UPDATE users SET steam_profile = '%s' WHERE username = '%s';"
                        % (up_steam, username) )
            print "Location: http://keycellar.drago.ninja/u/%s\n" % (username)
            
        else:
            #change to redirect back to profile
            print "Content-type: text/html\n"
            print_html_file("header.html")
            print "Invalid password!"
    elif not session or not session["session"].value:
        if login(username, password):
            session = create_session(username, password)
            print session.output()
            print "Location: http://keycellar.drago.ninja/u/%s\n" % (username)
        else:
            print_login_form(username, password)
    elif session:
        print_logout(username)
    else:
        print_login_form(username,password)

main()
