#! /usr/bin/python

import socket
import thread


s = socket.socket()
host = raw_input("Hostname: ")
port = int(raw_input("Port: "))


print 'CONNECTING TO SERVER.'

s.connect((host, port))
print s.recv(1024)

name = raw_input('Username: ')


def getMessages():
    global name
    while True:
        print "\r", s.recv(1024)


thread.start_new_thread(getMessages, ())

while True:
    message = raw_input('> ')
    if message == '/logout':
        s.send(message)
        print 'Logged out.'
        break
    s.send(name + '> ' + message)


s.close                     
