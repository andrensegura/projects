#!/usr/bin/python

import mysql
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256

#PRINTS OUT A FILE
def print_html_file(file_name):
    with open(file_name, 'r') as fin:
        print fin.read()

#DO STUFF WITH VARS
#PRINT STUFF TO GET VARS
print "Content-type: text/html\n"
print_html_file("/home/andre/domains/drago.ninja/header.html")
print_html_file("body.html")
