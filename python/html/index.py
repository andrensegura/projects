#!/usr/bin/python

import mysql #i wrote this
import cgi
import cgitb; cgitb.enable() #for troubleshooting
from passlib.hash import pbkdf2_sha256
from functions import print_html_file, print_header, get_cookie

def print_body():
    print_html_file("body.html")


print_header()
print_body()
