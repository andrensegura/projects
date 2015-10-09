#! /usr/bin/python


import socket
import thread

log = open('./server_log', 'w+')
newConnectionActive = False

#list of tuples. each element is a tuple of the form (addr, username)
#[client[0] for client in connectedClients] is synonymous to a list of client adresses
#[client[1] for client in connectedClients] is synonymous to a list of usernames
connectedClients = []

#returns a list of clients either 'byaddress' or 'byusername'
def listConnected(type):
    if type == 'byaddress':
        return [client[0] for client in connectedClients]
    elif type == 'byusername':
        return [client[1] for client in connectedClients]
    else:
        return 'listConnected: Invalid parameters : ' + 'given ' + type


def runCommand(command, commander, username):
    global connectedClients

    if command == '/help' or command == '/?':
        commander.send('List of commands:\n
                        /? or /help : shows commands\n
                        /connected : show all connected users\n
                        /whisper [target] [message] : whisper a user. duh. \n')
    elif command == '/connected':
        commander.send( 'Connected clients: ' + str(listConnected('byusername')) )
    elif command[:8] == '/whisper':
        command = command.split()
        toUser = command[1]
        message = ' '.join(command[2:])
        message = username + ' to ' +  toUser + '> ' + message
        if toUser == username:
            commander.send("Server: Can't whisper self.")
        elif toUser in listConnected('byusername'):
            commander.send(message)
            #lololol the logic for this one, man.
            recipient = listConnected('byaddress')[ listConnected('byusername').index(toUser) ]
            recipient.send(message)
            print >>log, message
        else:
            commander.send( 'Whisper target not found: ' + command[9:] )
    else:
        commander.send( 'Invalid Command' )


def connectClient(s):
    global newConnectionActive
    global connectedClients

    s.listen(5)
    print >>log, "Listening for clients.."
    c, addr = sock.accept()

    newConnectionActive = True

    user = c.recv(1024)
    message = 'New connection from "' + user + '"'
    print >>log, message + str(addr)
    for i in [client[0] for client in connectedClients]:
        i.send(message)

    connectedClients.append((c,user))

    while True:
        try:
            message = c.recv(1024)
            if message == '/logout':
                break
            elif message[0] == '/':
                runCommand(message, c, user)
            else:
                for i in [client[0] for client in connectedClients]:
                    i.send(user + '> ' + message)
                print >>log, user + '> ' + message
        except:
            break

    connectedClients.remove((c,user))
    c.close()
    message = user + ' logged out.'
    for i in [client[0] for client in connectedClients]:
        i.send(message)
    print >>log, message + str(addr)   

    return




print >>log, "Server starting up.."

sock = socket.socket()   
host = socket.gethostname()
port = 12345 
sock.bind((host, port))  

amountThreads = 0

try:
    thread.start_new_thread(connectClient, (sock, ))
except:
    print >>log, "Error: unable to start thread"

while True:
    if newConnectionActive == True:
        newConnectionActive = False
        try:
            thread.start_new_thread(connectClient, (sock, ))
        except:
            print >>log, "Error: unable to start thread"
    else:
        pass
