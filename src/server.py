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
from threading import Thread

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
Commandlist = [45,16384+20]
Commands = []
# Create a TCP/IP socket
rover = Rover  
Command_list=[]
clients = []
nicknames = []
point=0
Longitina =[]
Latina =[]
Alien =[]
x=0
y=0
sav_loc =[x,y]
sav_Rangle=0


def broadcast(message):
    try:
        message = message.to_bytes(2, byteorder = 'big', signed=False)
        tcpServer.send(message)
    except:
        print("nogo")

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 

    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print ("[+] New server socket thread started for " + ip + ":" + str(port))
 
    


    def run(self): 
        while True : 
            try:
                message = tcpServer.recv(1024)
                
                message = message.decode("ascii")
                print(message)
                
                message=str(message)
                opcode = message[0:3]
                

                if opcode == "UPM":
                    print("UPM received")
                    print("upm")
                    time.sleep(0.25)
                    msg=Commandlist[0]
                    broadcast(msg)
                    Commandlist.pop(0)
                    time.sleep(0.25)

                
                if opcode == "POS":
                    time.sleep(0.25)
                    print("in pos")
                    
                    message1 = tcpServer.recv(1024)
                    message1=int.from_bytes(message1, "big", signed="true")
                    message1=str(message1)
                    print('traveled: '+ message1)
                    # rover.distance = message1
                    time.sleep(0.25)
                    message2 = tcpServer.recv(1024)
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

                
            except:
                pass#
            finally:
                tcpServer.close()


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '192.168.43.192' 
TCP_PORT = 15000 
BUFFER_SIZE = 1024  #updating the stuff  

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print ("Multithreaded Python server : Waiting for connections from TCP clients...") 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 