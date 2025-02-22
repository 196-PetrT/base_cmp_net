#!/bin/python3
import socket
import time
import threading

# Connection Data

host = '192.168.0.101'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = [] # toDo попробовать dictionary?

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        # Accept Connection
        client, address = server.accept()
        # hostname = socket.gethostbyname(socket.gethostname()) # 
        print("Connected with {}".format(str(address)), ", " + itsatime)

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8') 
        # decode ascii string to unicode string and return it as unicode string with optional encoding 
        # toDo другие языки?
                
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast(("{} joined! " + " " + itsatime).format(nickname).encode('utf-8'))
        client.send(('Connected to server!' + " " + itsatime).encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()
