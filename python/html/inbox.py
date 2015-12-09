#! /usr/bin/python

import cgi
import mysql
from functions import print_header, get_session_user

username = get_session_user()
mail = mysql.execute_mysql("""SELECT * FROM mail WHERE recipient = %s OR sender = %s;"""
        , (username, username,) )

print_header()

if mail:
    for message in mail:
#        print """<table style="white-space:pre-wrap;">
#            <tr><td>From: %s</td></tr>
#            <tr><td>To: %s</td></tr>
#            <tr><td>Message:</td></tr>
#            <tr><td>%s</td></tr>
#            </table>""" % (message[1], message[2], message[4])
        print """<table style="white-space:pre-wrap;">
            <tr><td>From:</td><td>%s</td></tr>
            <tr><td>To:</td><td>%s</td></tr>
            <tr><td>Message:</td><td>%s</td></tr>
            </table>""" % (message[1], message[2], message[4])
        print "<br><hr><br>"
else:
    print "No mail! :("
