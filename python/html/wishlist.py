#!/usr/bin/python

import mysql #i wrote this
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from functions import print_header, get_session_user 
from steam import steam_search


username = get_session_user()
if not username:
    print "Location: https://keycellar.com/"


def get_games_list():
    print "<h2>Add games to %s's <b>wishlist</b>:</h2>" % (username)
    print """<form method="post" action="/add">
            Enter your list of games, separated by newlines:
            <br>
            <textarea cols="50" rows="20" name="games"></textarea>
            <br>
            <input type="submit" value="Add">
            </form>"""

def show_results(games_list):
    games_list = games_list.split('\r\n')

    print "<h2>Add games to %s's <b>wishlist</b>:</h2>" % (username)

    print """<form method="post" action="/wishlist">"""

    selected_games=0
    for game in games_list:
        print """<table class="add_games">"""
        results = steam_search(game)

        if not results: 
            print "No results found ( * A *)"
            continue

        #results.sort()
        print """<tr> 
                <td colspan="3"><h3 display="inline">Results for %s</h3></td></tr>""" % (game)
        
        checked=""" checked="checked" """
        good=False

        for app in results:
            
            if game.lower() not in app[0].lower():
                continue

            APPTITLE=0
            APPID=1
            APPIMG=2
            print """<tr>
                       <td><input type="radio" name="%s" value="%s" %s></td>
                       <td><a href="http://store.steampowered.com/app/%s/"><img src="%s"></a></td>
                       <td><a href="http://store.steampowered.com/app/%s/"><b>%s</b></a></td>
                    </tr>""" % (str(selected_games), app[APPID], checked, 
                                app[APPID], app[APPIMG], app[APPID], app[APPTITLE])
            checked=""
            good=True
        if not good:
            print """<tr><td colspan="3">No results found ( * A *)/</td></tr>"""
        print """<tr><td colspan="3"><hr></td></tr>"""
        print "</table>"
        selected_games += 1
    print """<input type="hidden" name="selected_games" value="%s">""" % (selected_games)
    print """<input type="submit" value="Add Selected Games">"""
    print "</form>"

def add_games(amt_games, user):
    from steam import get_game_info
    from ast import literal_eval
    import mysql

    games_list = mysql.execute_mysql("""SELECT wishlist FROM users WHERE username = %s"""
                   , (user,))[0][0]
    to_add = []

    for i in range(int(amt_games)):
        game_id = form.getvalue(str(i), "")
        to_add.append(get_game_info(game_id))

    if games_list:
        games_list = literal_eval(games_list)
        for game in games_list:
            if game not in to_add:
                to_add.append(game)

    mysql.execute_mysql("""UPDATE users SET wishlist = %s WHERE username = %s;"""
                        , (str(to_add), user,) )
    print "success!"

form = cgi.FieldStorage()
selected_games = form.getvalue("selected_games", "")
games = form.getvalue("games", "")

print_header()

if selected_games and selected_games != 0:
    add_games(selected_games, username)
elif games:
    show_results(games)
else:
    get_games_list()
