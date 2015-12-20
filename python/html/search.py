#! /usr/bin/python
import cgi
import cgitb; cgitb.enable() #for troubleshooting
import mysql
from functions import print_header, print_nav

def get_search_results(query):
    pass



print_header()

form = cgi.FieldStorage()
query = form.getvalue("search", "")

if query:
    print "<h2>Search: \"%s\"</h2>" % (query)
    s_query = "%" + query + "%"
    result = mysql.execute_mysql("""SELECT username, trades, steam_games
                                    FROM users WHERE steam_games LIKE %s;""", (s_query,) )
    if result:
        USERNAME=0;TRADES=1;GAMES=2
        print """<table class="search_table">
                <tr><td><b>Username</b></td>
                    <td><b>Trades</b></td>
                    <td><b>Matches</b></td></tr>"""
        for user in result:
            from ast import literal_eval
            games_list = []
            for game in literal_eval(user[GAMES]):
                if query.lower() in game[0].lower():
                    games_list.append(str("""<a href="%s">%s</a>""" % (game[1], game[0])))
            print ("""<tr class="highlight"><td valign="top"><a href="/u/%s">%s</a></td><td>%s</td>
                        <td valign="top">%s</td></tr>"""
                    % (user[USERNAME], user[USERNAME], user[TRADES], games_list ) )
        print "</table>"
    else:
        print "No results for \"%s\" found." % (query)
else:
    print "No results for \"%s\" found." % (query)
