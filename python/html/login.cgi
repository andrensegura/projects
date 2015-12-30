#!/usr/bin/python

import mysql, steam #files i wrote
import cgi, os, re
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256
from config import USERNAME, PASSWORD 
from functions import get_cookie, print_html_file, print_header, create_password_hash, get_session_user
from mycookie import create_session

#CHECKS LOG IN CRED, RETURNS TRUE ON SUCCESS
def login(user, passw):
    if not (user and passw):
        return False
    result = mysql.execute_mysql("""SELECT * FROM users WHERE username = %s""" , (user,))
    if not result:
        return False
    return pbkdf2_sha256.verify(passw, result[0][PASSWORD])

#LOGOUT
def logout(session):
    mysql.execute_mysql("""UPDATE users SET logged_in = '0' WHERE logged_in = %s;"""
                        , (session["session"].value,))
    session["session"] = ""
    session["session"]["domain"] = "keycellar.com"
    session["session"]["path"] = "/"
    session["session"]["expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    print session.output()
    print_lo()

def update_info(user, up_email, up_steam, up_hide):
    if up_hide:
        up_hide = 1
    mysql.execute_mysql("""UPDATE users SET hide_email=%s WHERE username = %s;"""
                , (up_hide, user,) )
    if re.match(r"[^@]+@[^@]+\.[^@]+", up_email):
        mysql.execute_mysql("""UPDATE users SET email = %s WHERE username = %s;"""
                , (up_email, user,) )
    if re.match(r"^[0-9]{17}$", up_steam):
        up_steam = steam.get_profile(up_steam)
        #set profile link
        mysql.execute_mysql("""UPDATE users SET steam_profile = %s WHERE username = %s;"""
                , (up_steam['profileurl'], user,) )
        #set avatar
        if up_steam['avatarmedium']:
            mysql.execute_mysql("""UPDATE users SET avatar = %s WHERE username = %s;"""
                    , (up_steam['avatarmedium'], user,) )
        #get tradeable games and catalog them
        games_list = steam.get_inventory(str(up_steam['profileurl'])) #doesn't work with unicode
        if games_list:
            try:
                result = mysql.execute_mysql("""SELECT steam_games FROM users WHERE username = %s;"""
                                        , (user,) )
                from ast import literal_eval
                result = literal_eval(result[0][1])
                games_list.append(result)
            except:
                pass
            games_list.sort()
            #strange thing when adding games. sometimes it has a bunch of empty
            #games which mess up a bunch of other things.
            for game in games_list:
                if len(game) == 0:
                    games_list.remove(game)
            mysql.execute_mysql("""UPDATE users SET steam_games = %s WHERE username = %s;""",
                            (str(games_list), user) )
    print "Location: http://keycellar.com/u/%s\n" % (user)

#RESET PASSWORD
def password_reset(reset, new_password, new_password2):
    import sys
    print_header()

    print """<div class="post">"""
    if not new_password or (new_password != new_password2) or (len(new_password) < 8):
        print """If the page simply refreshes, your inputs may not match, or your chosen password
                is less than 8 characters.<br>
                Enter new password:
                <form method="post" action="/login?reset=%s">
                <table>
                <tr><td>Password:</td><td><input type="password" name="new_pass"></td></tr>
                <tr><td>Confirm:</td><td><input type="password" name="new_pass2"></td></tr>
                <tr><td><input type="submit" value="Submit"></td><td>&nbsp;</td></tr>
                </table>
                </form>
              """ % (reset)
    else:
        pw_hash = create_password_hash(new_password)
        mysql.execute_mysql("""UPDATE users SET verified = '0', password = %s WHERE verified = %s;"""
                                , (pw_hash, reset,) )
        print """Password has been updated! <a href="/login">Log in!</a>"""
    sys.exit()

#PRINT LOGIN FORM
def print_login_form(user, passw):
    print_header()
    print """<div class="post">"""
    print_html_file("html/login.html")
    if user or passw:
        print "Invalid username or password."
    print "</div>"

def print_logout(user):
    print_header()
    print """<div class="post">"""
    print """Already logged in as %s!</a>""" % (user)
    print "</div>"

def print_lo():
    print_header()
    print """<div class="post">"""
    print_html_file("html/logout.html")
    print "</div>"

def main():
    #GET VARIABLES
    form = cgi.FieldStorage()
    username = form.getvalue("username", "")
    password = form.getvalue("password", "")
    action = form.getvalue("action", "")
    reset = form.getvalue("reset", "")
    
    if reset:
        np = form.getvalue("new_pass", "")
        np2 = form.getvalue("new_pass2", "")
        password_reset(reset,np,np2) 

    #CHECK COOKIE
    session = get_cookie()
    #i know there is a get_session_user() funtion i wrote, but this needs to be here instead
    if session:
        result = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
                   , (session["session"].value,))
        username = result[0][USERNAME] if result else username

    #DO STUFF WITH VARS
    if action == "logout" and session:
        logout(session)
    elif action == "update" and session:
        if login(username, password):
            up_email = form.getvalue("up_email", "")
            up_steam = form.getvalue("up_steam", "")
            up_hide = form.getvalue("hide_email", "")
            update_info(username, up_email, up_steam, up_hide)
        else:
            #change to redirect back to profile
            print_header()
            print "Invalid password!"
    elif not session or not session["session"].value:
        if login(username, password):
            session = create_session(username, password)
            print session.output()
            print "Location: http://keycellar.com/u/%s\n" % (username)
        else:
            print_login_form(username, password)
    elif session:
        print_logout(username)
    else:
        print_login_form(username,password)

main()
