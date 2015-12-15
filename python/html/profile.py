#!/usr/bin/python

import mysql, steam
from functions import print_header, print_html_file
import Cookie, os
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from config import USERNAME, EMAIL, TRADES, STEAM_PROFILE, LOGGED_IN, VERIFIED
from config import AVATAR, GAMES, HIDE_EMAIL, FRIENDS
from subprocess import Popen, PIPE, STDOUT

#CHECK USER
def check_user(user):
    result = mysql.execute_mysql("""SELECT * FROM users WHERE username = %s""" , (user,))
    if not result or not user:
        return "No such user here."
    return result[0]

def owns_profile(u_info, key):
    if key == u_info[LOGGED_IN]:
        return True
    else:
        return False 

def print_profile(info, sess_key, visitor):
    print """<div class="profile_details">"""
    print """<h1><img src="%s" alt=""> %s</h1>""" % (user_info[AVATAR] if user_info[AVATAR]
             else "/pics/princess.png", user_info[USERNAME])
    print """
        <table>
        %s
        <tr><td>Trades:</td><td>%s</td></tr>
        <tr><td>Steam Profile:</td><td>%s</td></tr>
        </table>
        """ % ("<tr><td>Email:</td><td>%s%s</td></tr>"
               % (info[EMAIL], "" if info[VERIFIED] == "0" else " (not verified)") if not info[HIDE_EMAIL]
               else "", info[TRADES], info[STEAM_PROFILE] )
    
    if owns_profile(user_info, sess_key):
        print_update_options(info)
    elif sess_key != "none" :
        print_contact_opts(info, visitor)

    print """</div>"""

def print_contact_opts(info, sess_key):
    visitor = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
                   , (session["session"].value,))[0]

    friend = form.getvalue("friend", "")
    if friend == "+Friends":
        #add friend
        from ast import literal_eval
        if visitor[FRIENDS]:
            visitor_friends = literal_eval(visitor[FRIENDS])
            visitor_friends.append(info[USERNAME])
        else:
            visitor_friends = "['%s']" % (info[USERNAME])
        mysql.execute_mysql("""UPDATE users SET friends=%s WHERE username=%s;""",
                             (str(visitor_friends), visitor[USERNAME],) )
    elif friend == "-Friends":
        #remove friend
        from ast import literal_eval
        visitor_friends = literal_eval(visitor[FRIENDS])
        visitor_friends.remove(info[USERNAME])
        mysql.execute_mysql("""UPDATE users SET friends=%s WHERE username=%s;""",
                            (str(visitor_friends), visitor[USERNAME]) )

    #refresh visitor
    visitor = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
                   , (session["session"].value,))[0]

    print """<form method="post" action="/u/%s"
            style="display:inline;margin:0px;padding:0px;">""" % (info[USERNAME])
    if info[USERNAME] not in visitor[FRIENDS]:
        print """<input type="submit" name="friend" value="+Friends">"""
    else:
        print """<input type="submit" name="friend" value="-Friends">"""
    print """</form>"""
    print """<input type="submit" name="new_message" value="Message"> """

def print_tradeables(info):
    print """<div class="tradeables">"""
    print "<br><b>Games Available for Trade:</b><br>"
    games_list = info[GAMES] 
    if games_list:
        from ast import literal_eval
        games_list = literal_eval(games_list)
        for game in games_list:
            print """<li><a href="%s">%s</a><br>""" % (game[1], game[0])
    else:
        print "No games in inventory or inventory is private."
    print """</div>"""

def print_update_options(info):
    print """<br><hr style="height:5px;border:none;color:silver;background-color:silver;">"""
    print """<div class="update_opts">"""
    print """
             <h2>Update your profile:</h2>
             <form method="post" action="/login?action=update">
             <input type="hidden" name="username" value="%s">

             <table>
             <tr><td>Hide Email:</td>
                <td><input type="checkbox" name="hide_email" value="1" %s></td></tr>
             <tr><td>Change Email:</td><td><input type="text" name="up_email"></td></tr>
             <tr><td colspan="2"><hr></td></tr>
             <tr><td>Enter current password:</td><td><input type="password" name="password"></td></tr>
             </table>
             <input type="submit" value="Update Settings">
             </form>
             <br>
         """ % (info[USERNAME], "checked" if info[HIDE_EMAIL] else "")
    print """<a href="/steam.php">Add tradeable games to library via Steam.</a>"""
    print """</div>"""

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("user", "")

#CHECK COOKIE
session = Cookie.SimpleCookie()
try:
    session.load(os.environ["HTTP_COOKIE"])
    result = mysql.execute_mysql(
               """SELECT * FROM users WHERE logged_in = %s"""
               , (session["session"].value,))
    if result:
        username = result[0][USERNAME] if username == "me" else username
except ((Cookie.CookieError, KeyError)):
    session = ""

#DO STUFF WITH VARS
#PRINT STUFF TO GET VARS
user_info = check_user(username)
print_header()
if user_info == "No such user here.":
    print user_info #which is just "No such user here."
else:
    if session:
        print_profile(user_info, session["session"].value, result[0][USERNAME])
    else:
        print_profile(user_info, "none")
    print_tradeables(user_info)
