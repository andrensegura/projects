#! /usr/bin/python
import cgi
import cgitb; cgitb.enable() #for troubleshooting
import mysql
from functions import print_header, print_nav

def search(query, type):
    if type == "steam_games":
        header = "Games added through Steam:"
    elif type == "added_games":
        header = "Games added manually:"
    elif type == "wishlist":
        header = "Games in users' wishlists:"

    if query:
        print "<h2>%s \"%s\"</h2>" % (header, query)
        s_query = "%" + query + "%"
        type = """SELECT username, trades, %s FROM users WHERE %s LIKE %%s;""" % (type, type)
        result = mysql.execute_mysql(type, (s_query,) )
        table_printed=False
        if result:
            for user in result:
                USERNAME=0;TRADES=1;GAMES=2
                TITLE=0; APPID=1; IMG=2
                from ast import literal_eval
                games_list = []
                for game in literal_eval(user[GAMES]):
                    if query.lower() in game[TITLE].lower():
                        games_list.append(str("""
                                <a href="http://store.steampowered.com/app/%s/">
                                  <img src="%s" width="120" height="45" alt=""></a>
                                <a href="http://store.steampowered.com/app/%s/">%s</a><br>
                                """ % (game[APPID], game[IMG], game[APPID], game[TITLE])))
                if games_list:
                    if not table_printed:
                        print """<table class="search_table">
                                <tr><td><b>Username</b></td>
                                <td><b>Trades</b></td>
                                <td><b>Matches</b></td></tr>"""
                        table_printed=True
                    print ("""<tr class="highlight"><td valign="top"><a href="/u/%s">%s</a></td>
                                <td valign="top">%s</td>
                                <td valign="top">%s</td></tr>"""
                            % (user[USERNAME], user[USERNAME], user[TRADES], ''.join(games_list) ) )
            print "</table>"
        else:
            print "No results for \"%s\" found." % (query)
        if not table_printed:
            print "No results for \"%s\" found." % (query)
    else:
        print "No results for \"%s\" found." % (query)


print_header()

form = cgi.FieldStorage()
query = form.getvalue("search", "")

if not query:
    print "No search query given."
else:
    search(query, "steam_games")
    search(query, "added_games")
    search(query, "wishlist")
