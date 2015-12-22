#!/usr/bin/python

import mysql, steam
from functions import print_header, print_html_file
import Cookie, os
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from config import * 

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

def print_profile(info, sess_key):
    print """<div class="profile_details">"""
    print """<h1><img src="%s" alt=""> %s</h1>""" % (info[AVATAR] if info[AVATAR]
             else "/pics/princess.png", info[USERNAME])
    print """
        <table>
        %s
        <tr><td>Trades:</td><td>%s</td></tr>
        <tr><td>Steam Profile:</td><td>%s</td></tr>
        </table>
        """ % ("<tr><td>Email:</td><td>%s%s</td></tr>"
               % (info[EMAIL], "" if info[VERIFIED] == "0" else " (not verified)") if not info[HIDE_EMAIL]
               else "", info[TRADES], info[STEAM_PROFILE] )
    
    print_friends(info[FRIENDS])
    if owns_profile(info, sess_key):
        print_update_options(info)
    elif sess_key != "none" :
        print_contact_opts(info, sess_key)

    print """</div>"""

def print_contact_opts(info, sess_key):
    visitor = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
                   , (session["session"].value,))[0]

    print """<form method="post" action="/u/%s"
            style="display:inline;margin:0px;padding:0px;">""" % (info[USERNAME])
    if info[USERNAME] not in visitor[FRIENDS]:
        print """<input type="submit" name="friend" value="+Friends"
                style="background-color:green;color:white;">"""
    else:
        print """<input type="submit" name="friend" value="-Friends"
                style="background-color:red;color:white;">"""
    print """</form>"""
    print """<form method="post" action="/inbox" style="display:inline;margin:0px;padding:0px;">
             <input type="hidden" name="id" value="new">
             <input type="hidden" name="pm" value="%s">
             <input type="submit" value="Message">
             </form>""" % (info[USERNAME])

def print_friends(friends_list):
    print """<div class="friends_list">"""
    if not friends_list:
        return
    from ast import literal_eval
    friends_list = literal_eval(friends_list)

    print """<table>
             <tr><td colspan="2"><b>Friends</b></td><td></tr>"""
    for friend in friends_list:
        avatar = mysql.execute_mysql("""SELECT avatar FROM users WHERE username = %s;""", (friend,) )
        if avatar[0][0] != "":
                avatar = avatar_info(friend, avatar[0][0])
        else:
                avatar = avatar_info(friend, "/pics/princess.png")
        print """<tr><td>%s</td><td valign="bottom left">
                 <a href="/u/%s">%s</a></td></tr>""" % (avatar, friend, friend)
    print "</table></div>"

def avatar_info(username, avatar):
    from ast import literal_eval
    user_info = check_user(username)
    if len(user_info[STEAM_GAMES]) > 0:
        amnt_st = len(literal_eval(user_info[STEAM_GAMES]))
    else:
        amnt_st = 0
    if len(user_info[ADDED_GAMES]) > 0:
        amnt_add = len(literal_eval(user_info[ADDED_GAMES]))
    else:
        amnt_add = 0
    if len(user_info[WISHLIST]) > 0:
        amnt_wsh = len(literal_eval(user_info[WISHLIST]))
    else:
        amnt_wsh = 0
    
    user_info="""<table>
            <tr><td>Trades:</td><td>%s</td></tr>
            <tr><td>Steam Games:</td><td>%s</td></tr>
            <tr><td>Added Games:</td><td>%s</td></tr>
            <tr><td>Wishlist:</td><td>%s</td></tr>
            </table>""" % (user_info[TRADES], amnt_st, amnt_add, amnt_wsh)

    avatar = """<span class="avatar">
                <a href="/u/%s">
                <img width="32" height="32" src="%s"></a>
                <div>%s</div></span>
                """ % (username, avatar, user_info)
    return avatar

def update_friends(info, friend, key):
    visitor = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
                   , (key,))[0]

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
    print """Location: http://keycellar.com/u/%s""" % (info[USERNAME])

def print_tradeables(info):
    TITLE=0; ID=1; PIC=2
    #print """<div class="tradeables">"""
    print """<div class="tabs">"""
    #print "<h2>Games Available for Trade</h2><hr>"

    print """<div class="options">
    <button onclick="show_content('first')" id="sel1">Steam</button>
    <button onclick="show_content('second')" id="sel2">Added</button>
    <button onclick="show_content('third')" id="sel3">Wishlist</button>
    </span>"""

    for inventory in range(STEAM_GAMES, WISHLIST+1):
        games_list = info[inventory] 
        try:
            from ast import literal_eval
            games_list = literal_eval(games_list)
        except:
            games_list = ""
        if games_list:
            if inventory == STEAM_GAMES:
                print """<div class="tab-content" id="first"><table>"""
            elif inventory == ADDED_GAMES:
                print """<div class="tab-content-hidden" id="second"><table>""" 
            elif inventory == WISHLIST:
                print """<div class="tab-content-hidden" id="third"><table>""" 
            for game in games_list:
                if not game:
                    continue
                print """<tr><td><img src="%s" width="120" height="45" alt=""></td>
                         <td valign="center">
                            <a href="http://store.steampowered.com/app/%s"><b>%s</b></a></td>
                         </td></tr>""" % (game[PIC], game[ID], game[TITLE])
            print "</table></div>"
        else:
            if inventory == STEAM_GAMES:
                print """<div class="tab-content" id="first"><table>"""
            elif inventory == ADDED_GAMES:
                print """<div class="tab-content-hidden" id="second"><table>"""
            elif inventory == WISHLIST:
                print """<div class="tab-content-hidden" id="third"><table>"""

            print """<tr><td>No games in this inventory.</td></tr></table></div>"""
    print """</div>"""

    print_html_file("show_content.js")
    print """<script>show_content('first')</script>"""

def print_update_options(info):
    print """<br>"""
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
    print """<a href="/steam.php">Add tradeable games to library via Steam.</a>
            <br>
            <a href="/add">Add games to library manually.</a>
            <br>
            <a href="/wishlist">Add games to wishlist.</a>"""
    print """</div>"""

#GET VARIABLES
form = cgi.FieldStorage()
username = form.getvalue("user", "")
friend = form.getvalue("friend", "")

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

if friend:
    update_friends(user_info, friend, session["session"].value)

print_header()
if user_info == "No such user here.":
    print user_info #which is just "No such user here."
else:
    if session:
        print_profile(user_info, session["session"].value)
    else:
        print_profile(user_info, "none")
    print_tradeables(user_info)
