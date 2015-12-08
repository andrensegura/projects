#!/usr/bin/python

import mysql #i wrote this
import mycookie #i wrote this
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256
from config import USERNAME

#PRINTS OUT A FILE
def print_html_file(file_name):
    with open(file_name, 'r') as fin:
        print fin.read()

def print_header():
    print "Content-type: text/html\n"
    print_html_file("header.html")

def print_nav(user):
    print """<a href="/">Home</a>"""
    print "&nbsp;|&nbsp;"
    if user:
        print """<a href="u/%s">%s</a>""" % (user, user)
        print """<a href="login?action=logout">(logout)</a>"""
        print "&nbsp;|&nbsp;"
    else:
        print """<a href="login">Log In</a>"""
        print "&nbsp;|&nbsp;"
    print """<a href="register"> Register</a>"""

def print_body():
    print_html_file("body.html")


username = ""
session = mycookie.get_cookie()

if session:
    result = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
               , (session["session"].value,))
    username = result[0][USERNAME] if result else username

print_header()
print "<hr>"
print_nav(username)
print "<hr>"
print_body()
