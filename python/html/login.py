#!/usr/bin/python

import mysql, steam #files i wrote
import cgi, os, string, re
import Cookie, datetime
import random
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256
from config import USERNAME, PASSWORD 
from functions import get_cookie, print_html_file, print_header, create_password_hash

#CHECKS LOG IN CRED, RETURNS TRUE ON SUCCESS
def login(user, passw):
    if not (user and passw):
        return False
    result = mysql.execute_mysql("""SELECT * FROM users WHERE username = %s""" , (user,))
    if not result:
        return False
    return pbkdf2_sha256.verify(passw, result[0][PASSWORD])

def create_session(user, passw):
    expires = datetime.datetime.now() + datetime.timedelta(days=3) 
    cookie = Cookie.SimpleCookie()
    random.seed(passw)
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)) 
    cookie["session"] = key
    cookie["session"]["domain"] = "keycellar.com"
    cookie["session"]["path"] = "/"
    cookie["session"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    #set key in database
    mysql.execute_mysql("""UPDATE users SET logged_in = %s WHERE username = %s;"""
                        , (key, user,) )
    return cookie

#PRINT LOGIN FORM
def print_login_form(user, passw):
    print_header()
    print_html_file("login.html")
    if user or passw:
        print "Invalid username or password."
def print_login_success(user):
    print_header()
    print_html_file("success.html")
    print """Proceed to your <a href="profile.cgi?user=%s">profile.</a>""" % (user)
def print_logout(user):
    print_header()
    print """Already logged in as %s!</a>""" % (user)
def print_lo():
    print_header()
    print_html_file("logout.html")

def main():
    #GET VARIABLES
    form = cgi.FieldStorage()
    username = form.getvalue("username", "")
    password = form.getvalue("password", "")
    action = form.getvalue("action", "")
    reset = form.getvalue("reset", "")
    
    if reset:
        import sys
        new_password = form.getvalue("new_pass", "")
        new_password2 = form.getvalue("new_pass2", "")
        print_header()
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
        

    #CHECK COOKIE
    session = get_cookie()
    if session:
        result = mysql.execute_mysql("""SELECT * FROM users WHERE logged_in = %s"""
                   , (session["session"].value,))
        username = result[0][USERNAME] if result else username

    #DO STUFF WITH VARS
    #PRINT STUFF TO GET VARS
    if action == "logout" and session:
        mysql.execute_mysql("""UPDATE users SET logged_in = '0' WHERE logged_in = %s;"""
                            , (session["session"].value,))
        session["session"] = ""
        session["session"]["domain"] = "keycellar.com"
        session["session"]["path"] = "/"
        session["session"]["expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        print session.output()
        print_lo()
    elif action == "update" and session:
        if login(username,password):
            up_email = form.getvalue("up_email", "")
            up_steam = form.getvalue("up_steam", "")
            up_hide = form.getvalue("hide_email", "")
            if up_hide:
                up_hide = 1
            mysql.execute_mysql("""UPDATE users SET hide_email=%s WHERE username = %s;"""
                        , (up_hide, username,) )
            if re.match(r"[^@]+@[^@]+\.[^@]+", up_email):
                mysql.execute_mysql("""UPDATE users SET email = %s WHERE username = %s;"""
                        , (up_email, username,) )
            if re.match(r"^[0-9]{17}$", up_steam):
                up_steam = steam.get_profile(up_steam)
                #set profile link
                mysql.execute_mysql("""UPDATE users SET steam_profile = %s WHERE username = %s;"""
                        , (up_steam['profileurl'], username,) )
                #set avatar
                if up_steam['avatarmedium']:
                    mysql.execute_mysql("""UPDATE users SET avatar = %s WHERE username = %s;"""
                            , (up_steam['avatarmedium'], username,) )
                #get tradeable games and catalog them
                games_list = steam.get_inventory(str(up_steam['profileurl'])) #doesn't work with unicode
                if games_list:
                    try:
                        result = mysql.execute_mysql("""SELECT steam_games FROM users WHERE username = %s;"""
                                                , (username,) )
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
                                    (str(games_list), username) )
            print "Location: http://keycellar.com/u/%s\n" % (username)
            
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
