#! /usr/bin/python

import sys
import socket
import thread
from commands import runCommand

############################
#   VARIABLES              #
############################

#ERROR CONSTANTS
THREAD_NOT_STARTED = 1
INVALID_PARAMETER = 2

newConnectionActive = False


#list of tuples. each element is a tuple of the form (addr, username)
#[client[0] for client in connectedClients] is synonymous to a list of adresses
#[client[1] for client in connectedClients] is synonymous to a list of usernames
connectedClients = []



############################
#   FUNCTIONS              #
############################

''' function Error(int err num, name of function that called it)
expects an integer corresponding to one of the 'constants' listed at the top of
the script. The constant refers to a number that gives details of the error raised.
''' #i know there is a better way to do this type of thing. im just dumb. will fix eventually.

def Error(intErrorCode, function):
    if intErrorCode == THREAD_NOT_STARTED:
        print >>sys.stderr, function + ": Error: unable to start thread."
    elif intErrorCode == INVALID_PARAMETER:
        print >>sys.stderr, function + ': Invalid parameters'
    elif not isinstance(intErrorCode, int):
        print >>sys.stderr, "Error code invalid."




''' function listConnected(string 'byaddress' or 'byusername')
returns a list of clients either 'byaddress' or 'byusername'
'''

def listConnected(type):
    if type == 'byaddress':
        return [client[0] for client in connectedClients]
    elif type == 'byusername':
        return [client[1] for client in connectedClients]
    else:
        Error(INVALID_PARAMETER, 'listConnected')


'''function relayAll(sender username or 'server', message to send)
sends the message to all connected clients, including printing it
to the server
'''

def relayAll(username, msg):
    if username == 'server':
        msg = 'Server: ' + msg
    else:
        msg = username + '> ' + msg

    for i in listConnected('byaddress'):
        i.send(msg)
    print msg


''' function connectClient(socket)
receives a socket variable and starts listening for a client.
when it receives a connection, then it starts a loop to
get messages.
'''

def connectClient(s):
    global newConnectionActive
    global connectedClients

    s.listen(5)
    print "Listening for clients.."
    c, addr = s.accept()

    newConnectionActive = True

    user = c.recv(1024)
    message = 'New connection from "' + user + '"'
    print(str(addr)),                               #adding a trailing comma prevents a newline.
    relayAll('server', message)

    connectedClients.append((c,user))

    while True:
        try:
            message = c.recv(1024)
            if message == '/logout':
                break
            elif message[0] == '/':
                runCommand(message, c, user, listConnected('byaddress'), listConnected('byusername'))
            else:
                relayAll(user, message)
        except:
            break

    connectedClients.remove((c,user))
    c.close()
    message = user + ' logged out.'
    print (str(addr)),
    relayAll('server', message)

    return



def main():
    global newConnectionActive

    print "Server starting up.."

    sock = socket.socket()   
    host = socket.gethostname()
    port = 12345 
    sock.bind((host, port))  


    try:
        thread.start_new_thread(connectClient, (sock, ))
    except:
        Error(THREAD_NOT_STARTED, 'main') 
    while True:
        if newConnectionActive == True:
            newConnectionActive = False
            try:
                thread.start_new_thread(connectClient, (sock, ))
            except:
                Error(THREAD_NOT_STARTED, 'main')
        else:
            pass


if __name__ == "__main__":
    main()
