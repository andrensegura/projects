#!/usr/bin/python

import smtplib
import email.utils
from email.mime.text import MIMEText

def email_new_account(address, username, verify_link):
    sender = "andre@keycellar.com" 
    receivers = [address]

    msg = MIMEText("""
Hello %s,

You are receiving this message because the email address

%s

was used to sign up for an account on http://keycellar.com. If
you did NOT sign up for this service, please reply to this email and
let me know. I will remove the user as soon as I am aware. Other than
this signup notice, you will not receive any emails from this domain
until the account is verified, so you do not need to worry about spam.

In order to verify your account, please follow the link below and sign in:

%s

Thank you for your interest in this service! :)

With love,


Andre Segura
""" % (username, address, verify_link) )

    #the following three lines are to make sure that the email is RFC compliant.
    msg['To'] = email.utils.formataddr(('', address))
    msg['From'] = email.utils.formataddr(('Andre Segura', sender))
    msg['Subject'] = 'KeyCellar New Account Verification Notice'

    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receivers, msg.as_string())         
    except SMTPException:
       print "Error: unable to send email"
