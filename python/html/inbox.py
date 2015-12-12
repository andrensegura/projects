#! /usr/bin/python

import cgi
import mysql
from config import ID, IS_READ, SENDER, RECIPIENT, TIME, SUBJECT, BODY
from functions import print_header, get_session_user, is_verified


#SORT METHODS
def get_unread(mail, user):
    unread = []
    for message in mail:
        if (not message[IS_READ]) and (message[RECIPIENT] == user):
            unread.append(message)
    return unread

def get_sent(mail, user):
    sent = []
    for message in mail:
        if message[SENDER] == user:
            sent.append(message)
    return sent

def get_received(mail, user):
    received = []
    for message in mail:
        if message[RECIPIENT] == user:
            received.append(message)
    return received

#PRINT MAIL
def print_mail(mail):
    for message in mail:
        if message[IS_READ] or message[SENDER] == username:
            print """<table style="white-space:pre-wrap;">"""
        else:
            print """<table style="white-space:pre-wrap;" bgcolor="#f2f2f2">"""
        print """
            <tr><td>From:</td><td valign="left" width="100%%">%s</td></tr>
            <tr><td>To:</td><td valign="left">%s</td></tr>
            <tr><td>Time:</td><td valign="left">%s</td></tr>
            <tr><td valign="top">Subject:</td><td valign="left">%s</td></tr>
            <tr><td valign="top">Message:</td><td valign="left">%s</td></tr>
            </table>""" % (message[SENDER], message[RECIPIENT], message[TIME], message[SUBJECT], message[BODY])
        if message[RECIPIENT] == username:
            print """
                <form method="post" style="display:inline;margin:0px;padding:0px;" action="/inbox">
                    <input type="hidden" name="id" value="%s">
                    <input type="submit" value="Reply">
                </form>
                """ % (message[ID])
            if not message[IS_READ]:
                print """
                    &nbsp;
                    <form method="post" style="display:inline;margin:0px;padding:0px;" action="/inbox">
                        <input type="hidden" name="mar" value="%s">
                        <input type="submit" value="Mark as read">
                    </form>
                    """ % (message[ID])
        print "<br><hr><br>"

def print_compose(user, id=0):
    if id == 0:
        mail = mysql.execute_mysql("""SELECT * FROM mail WHERE id = %s;"""
            , (id,) )[0] 
    else:
        mail = mysql.execute_mysql("""SELECT * FROM mail WHERE id = %s AND recipient = %s;"""
            , (id, user,) )[0]
        mail = list(mail)
        mail[SUBJECT] = "Re: " + mail[SUBJECT]
        mail[BODY] = "\n\n\n\n--------------\nQuote:\n" + mail[BODY]
    print """
        <form method="post" action="/inbox">
            <input type="hidden" name="sender" value="%s">
            <table style="white-space:pre-wrap;">
                <tr><td>From:</td>
                    <td>%s</td></tr>
                <tr><td>To:</td>
                    <td><input type="text" name="recipient" value="%s"</td></tr>
                <tr><td>Subject:</td>
                    <td><input type="text" name="subject" value="%s"></td></tr>
                <tr><td valign="top">Message:</td>
                    <td><textarea cols="50" rows="10" name="body">%s</textarea>
                        </td></tr>
                <tr><td>&nbsp;</td>
                    <td><input type="submit" name="send" value="Send"></td></tr>
            </table>
        </form>
        """ % (user, user, mail[SENDER], mail[SUBJECT], mail[BODY])

username = get_session_user()
form = cgi.FieldStorage()
sort_by = form.getvalue("sort", "")
compose = form.getvalue("id", "")
send = form.getvalue("send", "")
mar = form.getvalue("mar", "")

if mar:
    mysql.execute_mysql("""UPDATE mail SET is_read = '1' WHERE id = %s;""", (mar,) ) 

print_header()

if not is_verified(username):
    print "Mail functionality is not available to un-verified users. (  * A * )/"
    import sys; sys.exit()

print """
    <a href="/inbox?sort=unread">Unread</a> - 
    <a href="/inbox?sort=sent">Sent</a> - 
    <a href="/inbox?sort=received">Received</a> - 
    <a href="/inbox?sort=all">All</a> 
    <br> <a href="/inbox?id=new">New Message</a>
    <br>
    <br>
    """

if send:
    sender = form.getvalue("sender", "")
    recipient = form.getvalue("recipient", "")
    subject = form.getvalue("subject", "(No Subject)")
    body = form.getvalue("body", "")

    if not sender:
        print "Somehow, your username wasn't picked up."
    elif not recipient:
        print "Recipient needed!"
    elif not body:
        print "Need message body."
    else:
        mysql.execute_mysql("""INSERT INTO mail (sender, recipient, subject, body, is_read)
                            VALUES (%s, %s, %s, %s, %s);""", (sender, recipient, subject, body, '0'))
        print "Sent!"
elif compose == "new":
        print_compose(username) 
elif compose:
        print_compose(username, compose) 
else:
    mail = mysql.execute_mysql("""SELECT * FROM mail WHERE recipient = %s OR sender = %s;"""
        , (username, username,) )
    if mail:
        if sort_by == "unread":
            sorted_mail = get_unread(mail, username)
        elif sort_by == "sent":
            sorted_mail = get_sent(mail, username)
        elif sort_by == "received":
            sorted_mail = get_received(mail, username)
        elif sort_by == "all":
            sorted_mail = mail 
        else:
            sorted_mail = get_unread(mail, username)
            if not sorted_mail:
                sorted_mail = mail

        if sorted_mail:
            print_mail(sorted_mail)
        else:
            print "No messages in '%s'." % (sort_by)
    else:
        print "No mail! :("
