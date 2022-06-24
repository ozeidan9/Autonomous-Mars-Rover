from http import server
from re import I
import socket
import threading
from automate import Rover
from yap import update
import yap
import time
import automate
import numpy as np

map = np.zeros((240,360))
# autogen = True
z=0
count = 0
global autogen, restart, sav_dist

autogen = True
restart = False
sav_dist=0
# restart = False

#omar make sure you add these to the angle and distance you get
Commandlist = [45,20]
Commands = []
# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.43.50', 15000)
# print('starting up on port ' + server_address[0] + server_address[1])
server.bind(server_address)
# Listen for incoming connections
server.listen(1)

rover = Rover  


clients = []
nicknames = []
point=0

Longitina =[]
Latina =[]
Alien =[]
# sav_dist=0
x=0
y=0
sav_loc =[x,y]
sav_Rangle=0



def broadcast(message):

    try:
        for client in clients:
            #message = message.encode('ascii')
            points_bytes = message.to_bytes(2, byteorder = 'big', signed=True)
            client.send(message)
    except:
        #need to fix it, summit bout a while loop and flags. 
        client, address = server.accept()
        print("connected to " + str(address))

        #client.send('Nick'.encode('ascii'))
        nickname  = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

def handle(client):
    i = 0
    while True:
        try:
            message = client.recv(1024)
            
            message = message.decode("ascii")
            print(message)
            time.sleep(0.25)
            message=str(message)
            opcode = message[0:3]
            

            if opcode == "UPM":
                msg=Commandlist[0]
                broadcast(msg)
                Commandlist.pop(0)

            
            if opcode == "POS":
                print("in pos")
                
                message1 = client.recv(1024)
                message1=int.from_bytes(message1, "big", signed="true")
                message1=str(message1)
                print('traveled: '+ message1)
                # rover.distance = message1
                time.sleep(0.25)
                message2 = client.recv(1024)
                message2=int.from_bytes(message2, "big", signed="true")
                message2=str(message2)
                print('angle:'+message2)
                time.sleep(0.25)
                # rover.angle = message2
                # Rangle=message2
                # dist=message2-sav_dist
                # loc=yap.calc_loc(Rangle,sav_dist,dist,sav_loc)
                # rover.x=loc[0]
                # rover.y=loc[1]
                # print('x:'+rover.x)
                # print('y:'+rover.y)
                
                # if (Rangle!=sav_Rangle):
                #     sav_loc=loc
                #     sav_Rangle=Rangle
                #     sav_dist=dist
        
            exit (1)
            
        except:
            exit(1)


def receive():
    while True:
        client, address = server.accept()
        print("connected to " + str(address))

        #client.send('Nick'.encode('ascii'))
        nickname  = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        


        print("Nickname of client is " + nickname)
        # broadcast((nickname +  "joined the chat!").encode('ascii'))
        # client.send("connected to server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()




print("Server is listening...")
receive()