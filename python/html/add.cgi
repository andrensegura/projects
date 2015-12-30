#!/usr/bin/python

import mysql #i wrote this
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from functions import print_header, get_session_user 
from steam import steam_search


username = get_session_user()
if not username:
    print "Location: https://keycellar.com/"


def get_games_list(wishlist=False):
    print "<h2>Add games to %s's %s:</h2>" % (username, "wishlist" if wishlist else "library")
    print """<form method="post" action="/%s">
            Enter your list of games, separated by newlines:
            <br>
            <textarea cols="50" rows="20" name="games"></textarea>
            <br>
            <input type="submit" value="Add">
            </form>""" % ("wishlist" if wishlist else "add")

def show_results(games_list, wishlist=False):
    games_list.strip()
    games_list = games_list.split('\r\n')

    print "<h2>Add games to %s's %s:</h2>" % (username, "wishlist" if wishlist else "library")

    print """<form method="post" action="/%s">""" % (username, "wishlist" if wishlist else "library")

    selected_games=0
    for game in games_list:
        game.strip()
        print """<table class="add_games">"""
        results = steam_search(game)

        #results.sort()
        print """<tr> 
                <td colspan="3"><h3 display="inline">Results for %s</h3></td></tr>""" % (game)
        
        checked=""" checked="checked" """

        good=False

        for app in results:
            import string
            game_stripped = game.translate(string.maketrans("",""), string.punctuation).lower()
            game_stripped = "".join(game_stripped.split())
            app_stripped =  app[0].translate(string.maketrans("",""), string.punctuation).lower()
            app_stripped = "".join(app_stripped.split())
            if (game_stripped not in app_stripped): 
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

def add_games(amt_games, user, wishlist=False):
    from steam import get_game_info
    from ast import literal_eval
    import mysql

    mysql_query = """SELECT %s FROM users WHERE username = %%s;""" % ("wishlist"
                    if wishlist else "added_games") 
    games_list = mysql.execute_mysql(mysql_query, (user,))[0][0]
    to_add = []

    for i in range(int(amt_games)):
        game_id = form.getvalue(str(i), "")
        game = get_game_info(game_id)
        if game:
           to_add.append(game)
        else:
            print "Game ID %s probably requires an age check." % (game_id)

    if games_list:
        games_list = literal_eval(games_list)
        for game in games_list:
            if game not in to_add:
                to_add.append(game)

    mysql_query = """UPDATE users SET %s = %%s WHERE username = %%s;""" % ("wishlist"
                    if wishlist else "added_games")
    mysql.execute_mysql(mysql_query, (str(to_add), user,) )
    print "<br>Success!"

def main():
    form = cgi.FieldStorage()
    selected_games = form.getvalue("selected_games", "")
    games = form.getvalue("games", "")
    wishlist = form.getvalue("wishlist", "")

    print_header()
    print """<div class="post">"""

    if selected_games and selected_games != 0:
        add_games(selected_games, username, wishlist)
    elif games:
        show_results(games, wishlist)
    else:
        get_games_list(wishlist)

    print "</div>"


main()
