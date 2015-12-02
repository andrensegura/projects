#!/usr/bin/python

import mysql, steam
import Cookie, os
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from dbstructure import USERNAME, EMAIL, TRADES, STEAM_PROFILE, LOGGED_IN, VERIFIED

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
    if key == u_info[LOGGED_IN]:
        return True
    else:
        return False 

#PRINT LOGIN FORM
def print_profile(user, info):
    print "Content-type: text/html\n"
    print_html_file("header.html")
    print_html_file("profile.html")
    print """
<table>
<tr><td>Username:</td><td>%s</td></tr>
<tr><td>Email:</td><td>%s (%s)</td></tr>
<tr><td>Trades:</td><td>%s</td></tr>
<tr><td>Steam Profile:</td><td>%s</td></tr>
</table>
""" % (info[USERNAME], info[EMAIL], "verified" if info[VERIFIED] == "0" else "not verified", 
       info[TRADES], info[STEAM_PROFILE] )

    print "<br><b>Games Available for Trade:</b><br>"
    games_list = steam.get_inventory(info[STEAM_PROFILE])
    if games_list:
        for game in games_list:
            print """<li><a href="%s">%s</a><br>""" % (game[1], game[0])
    else:
        print "No games in inventory or inventory is private."

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("user", "")
up_email = form.getvalue("up_email", "")
up_steam = form.getvalue("up_steam", "")

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
    print_html_file("header.html")
    print user_info #which is just "No such user here."
elif not session:
    print_profile(username, user_info)
elif owns_profile(user_info, session["session"].value):
    print_profile(username, user_info)
    print """<br>
             <h2>Update your settings:</h2>
             <form method="post" action="http://keycellar.drago.ninja/login?action=update">"""
    print """<input type="hidden" name="username" value="%s">""" % (username)
    print_html_file("updatesettings.html")
    print "</form>"
else:
    print_profile(username, user_info)
