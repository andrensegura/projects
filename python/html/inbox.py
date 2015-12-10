#! /usr/bin/python

import cgi
import mysql
from config import IS_READ, SENDER, RECIPIENT, SUBJECT, BODY
from functions import print_header, get_session_user

username = "faroeson" #get_session_user()
mail = mysql.execute_mysql("""SELECT * FROM mail WHERE recipient = %s OR sender = %s;"""
        , (username, username,) )

print_header()

if mail:
    for message in mail:
        if message[IS_READ] or message[SENDER] == username:
            print """<table style="white-space:pre-wrap;">"""
        else:
            print """<table style="white-space:pre-wrap;" bgcolor="#f2f2f2">"""
        print """ 
            <tr><td>From:</td><td valign="left" width="100%%">%s</td></tr>
            <tr><td>To:</td><td valign="left">%s</td></tr>
            <tr><td valign="top">Subject:</td><td valign="left">%s</td></tr>
            <tr><td valign="top">Message:</td><td valign="left">%s</td></tr>
            </table>""" % (message[SENDER], message[RECIPIENT], message[SUBJECT], message[BODY])
        print "<br><hr><br>"
else:
    print "No mail! :("
