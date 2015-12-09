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
    result = mysql.execute_mysql("""SELECT username, trades FROM users WHERE games LIKE %s;""", (s_query,) )

    if result:
        print "<table>"
        for user in result:
            print ("""<tr><td><li><a href="/u/%s">%s</a></td><td>(trades: %s)</td></tr>"""
                    % (user[0], user[0], user[1]) )
        print "</table>"
    else:
        print "No results for \"%s\" found." % (query)
else:
    print "No results for \"%s\" found." % (query)
