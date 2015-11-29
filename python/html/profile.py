#!/usr/bin/python

import mysql
import Cookie, os
import cgi
import cgitb; cgitb.enable() #for troubleshooting

#PRINTS OUT A FILE
def print_html_file(file_name):
    with open(file_name, 'r') as fin:
        print fin.read()

#CHECK USER
def check_user(user):
    result = mysql.execute_mysql("SELECT * FROM users WHERE username = '%s'" % (user))
    if not result or not user:
        return "No such user here."
    return result[0]

def owns_profile(u_info, key):
    if key == u_info[7]:
        return True
    else:
        return False 

#PRINT LOGIN FORM
def print_profile(user, info):
    print "Content-type: text/html\n"
    print_html_file("/home/andre/domains/drago.ninja/header.html")
    print_html_file("profile.html")
    print """
<table>
<tr><td>Username:</td><td>%s</td></tr>
<tr><td>Email:</td><td>%s (%s)</td></tr>
<tr><td>Trades:</td><td>%s</td></tr>
<tr><td>Game List:</td><td>%s</td></tr>
<tr><td>Steam Profile:</td><td>%s</td></tr>
</table>
""" % (info[0], info[2], "verified" if info[6] == 0 else "not verified", 
       info[5], info[3], info[4] )

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("user", "")
session = form.getvalue("sess", "")

#CHECK COOKIE
session = Cookie.SimpleCookie()
try:
    session.load(os.environ["HTTP_COOKIE"])
    result = mysql.execute_mysql(
               "SELECT * FROM users WHERE logged_in = '%s'"
               % (session["session"].value))
except ((Cookie.CookieError, KeyError)):
    session = ""

#DO STUFF WITH VARS
#PRINT STUFF TO GET VARS
user_info = check_user(username)
if user_info == "No such user here.":
    print "Content-type: text/html\n"
    print_html_file("/home/andre/domains/drago.ninja/header.html")
    print user_info
elif owns_profile(user_info, session["session"].value):
    print_profile(username, user_info)
    print "<br>This is your profile!"
else:
    print_profile(username, user_info)
