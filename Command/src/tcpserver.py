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
Commandlist = []
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

def rov_decode(message1):
    message1=int.from_bytes(message1, "big", signed="true")
    message1=str(message1)
    return message1

def broadcast(message):

    try:
        for client in clients:
            message = message.encode('ascii')
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
            #print("in handle")
            message = client.recv(1024)
            
            message = message.decode("ascii")
            print(message)
            message=str(message)
            opcode = message[0:3]

            if opcode == "MOVU":
                Commandlist.append("1")
                
            if opcode == "MOVL":
                Commandlist.append("2")

            if opcode == "MOVR":
                Commandlist.append("3")

            if opcode == "MOVD":
                Commandlist.append("4")

            if message == "POS":
                print("in pos")
                time.sleep(1)
                message1 = client.recv(1024)
                message1=int.from_bytes(message1, "big", signed="true")
                message1=str(message1)
                print('traveled: '+ message1)
                rover.distance = message1
                
                time.sleep(1)
                message2 = client.recv(1024)
                message2=int.from_bytes(message2, "big", signed="true")
                message2=str(message2)
                print('angle:'+message2)
                rover.angle = message2
                Rangle=message2
                dist=message2-sav_dist
                loc=yap.calc_loc(Rangle,sav_dist,dist,sav_loc)
                rover.x=loc[0]
                rover.y=loc[1]
                print('x:'+rover.x)
                print('y:'+rover.y)
                
                if (Rangle!=sav_Rangle):
                    sav_loc=loc
                    sav_Rangle=Rangle
                    sav_dist=dist
                
                message4 = client.recv(1024)
                message4=int.from_bytes(message4, "big", signed="true")
                message4=str(message4)
                
            if opcode== "IDA":
                print ("ida")
                message1 = client.recv(1024)
                message1=int.from_bytes(message1, "big", signed="true")
                message1=str(message1)
                print("dist:" + message1)
                colour='#FF0000'
                yap.alien(x,y,Rangle,colour,dist,Longitina,Latina,Alien)

            if opcode=="RAD":
                message4 = client.recv(1024)
                message4=int.from_bytes(message4, "big", signed="true")
                message4=str(message4)
                print("dist:" + message4)
                yap.alien(x,y,Rangle,'#000000',dist,Longitina,Latina,Alien)
            

            # yap.alien(x,y,Rangle,'#ffffff',0,0,Longitina,Latina,Alien)
            

            if opcode=="MODA":
                Commandlist.clear()
                autogen = True


            if opcode=="MODM":
                Commandlist.clear()
                autogen = False


            if opcode[0:3]=="START":
                point = automate.update_start(opcode[3:6], opcode[6:9], opcode[9:12]) # x,y,angle

                
            #19, 16, 13 circ, 22 degree from center

            time.sleep(1)
            #     # x=int(message[3:6])
            #     # # print(x)
            #     # y=int(message[6:9])
            #     # #print(y)
            #     # Rangle=int(message[9:12])
            #     # #print(Aangle)
            #     # yap.alien(x,y,Rangle,'#ffffff',0,0,Longitina,Latina,Alien)
           
            # if opcode == "IDA":a
            #    #level="IDA"+"010"+"024"+"045"+"ff00ff"+"001"+"28"+"28"+"1"
            #     x=int(message[3:6])
            #     # print(x)
            #     y=int(message[6:9])
            #     #print(y)
            #     Aangle=int(message[9:12])
            #     #print(Aangle)
            #     colour='#'+message[12:18]
            #     #print(colour)
            #     Rangle=int(message[18:21])
            #     #print(Rangle)
            #     dist=int(message[21:25])
            #     dist=float(dist/100)
            #     #print(dist)
            #     yap.alien(x,y,Rangle,colour,Aangle,dist,Longitina,Latina,Alien)
            #     #yap.draw(Longitina, Latina, Alien)
            #     #print(Longitina[0])
            #     # f = open("Command/src/components/Map.js", "a")
            #     # f.close()
            #     # f.close()
            
            # if opcode == 'BAT':
                
            #     level_val = message[3:6]

            #     print("recieved battery level")
                
            #     infile = open('components/Level.js','r+')
            #     content = infile.readlines() #reads line by line and out puts a list of each line
            #     content[3] = 'let inputval = ' + level_val + ';' #replaces content of the 2nd line (index 1)
            #     infile.close()
            #     infile = open('components/Level.js', 'w') #clears content of file. 
            #     infile.close
            #     infile = open('components/Level.js', 'r+')
            #     for item in content: #rewrites file content from list 
            #         infile.write("%s" % item)
            #     infile.close()
            # else:
            exit (1)
            


        except:
            if autogen is True:
                list_size =len(Commandlist)
                if restart == False:
                    msg = Commandlist[0]
                    broadcast(msg)
                    Commandlist.pop(0)
                    if list_size != 0:
                        switch = False
                        
                    if list_size == 0:
                        s=(s-1)*-1
                        if s==2: #start state
                            index = point%8
                            next_path = automate.automate_route(map, [rover.x, rover.y], automate.poi[index])
                            # send to drive
                            s=0

                        if s==1: #investgate
                            Commands=automate.exe()
                            while z <len(Commands):
                                Commandlist.append(Commands[z])
                            z=0
                            
                            
                        if s==0:#move to point
                            count = count + 1
                            index = (point+count)%8
                            next_path = automate.automate_route(map, [rover.x, rover.y], automate.poi[index])
                            while z <len(next_path):
                                Commandlist.append(next_path[z])
                            z=0
                                
                if restart==True:
                    Commandlist.clear()
            if autogen == False:
                print(input)

                #for manual ctrl

        

            

            # print('your mom')
            # index = clients.index(client)
            # clients.remove(client)
            # client.close()
            # nickname = nicknames[index]
            # # broadcast((nickname + "left the chat!").encode('ascii'))
            # nicknames.remove(nickname)
            # break

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