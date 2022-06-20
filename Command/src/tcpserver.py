from http import server
from re import I
import socket
import threading
from Command.src.automate import Rover, dead_zone
import yap
import time
import automate 


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.43.192', 15000)
# print('starting up on port ' + server_address[0] + server_address[1])
server.bind(server_address)
# Listen for incoming connections
server.listen(1)

clients = []
nicknames = []

rover = Rover  

Longitina =[]
Latina =[]
Alien =[]
sav_dist=0
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

            if opcode == "MOV" or "MOD":
                # broadcast(message)
                print(message)
                client = clients[1]
                client.send(message)


            if opcode == "vof" or "rof":  #if vision or radar is toggled OFF from app
                # broadcast(message)
                print(message)
                client = clients[1]
                client.send(message)

            if opcode == "von" or "ron":  #if vision or radar is toggled ON from app
                # broadcast(message)
                print(message)
                client = clients[1]
                client.send(message)


            if message == "POS":
                print("in pos")
                time.sleep(1)
                message1 = client.recv(1024)
                message1=int.from_bytes(message1, "big", signed="true")
                message1=str(message1)
                print('traveled: '+ message1)
                Rangle=message1
                rover.y = message1 # updates current y position
                time.sleep(1)
                message2 = client.recv(1024)
                message2=int.from_bytes(message2, "big", signed="true")
                message2=str(message2)
                print('angle:'+message2)
                rover.angle = message2 # updates current angle position
                dist=message2-sav_dist
                # loc=yap.calc_loc(Rangle,sav_dist,dist,sav_loc)
                # x=loc[0]
                # y=loc[1]
                # print('x:'+x)
                # print('y:'+y)
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


                # dead_zone(map, [0,0]) # add coordinate of alien to dead zone on map

            if opcode=="RAD":
                message4 = client.recv(1024)
                message4=int.from_bytes(message4, "big", signed="true")
                message4=str(message4)
                print("dist:" + message4)
                yap.alien(x,y,Rangle,'#000000',dist,Longitina,Latina,Alien)
            

            yap.alien(x,y,Rangle,'#ffffff',0,0,Longitina,Latina,Alien)
                

                
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
            if i %5==1:
                msg = str("4")
                broadcast(msg)
            if i %5==2:
                msg = str("1")
                broadcast(msg)
            if i %5==3:
                msg = str("2")
                broadcast(msg)
            if i %5==4:
                msg = str("3")
                broadcast(msg)
            else:
                broadcast("0")
            i = i+1

            

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