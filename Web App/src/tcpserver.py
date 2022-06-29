from ctypes import pointer
from re import I
import socket
import threading
#from automate import Roverfrom yap import update
import numpy as np
from threading import Thread
import math
#import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import time
import automate
import yap
# from automate import *
##multii thread this
aliens=0 
drawin=0
map=np.zeros((360,240))
autogen = 0
angle=0
point=0
needmore=1
sav_loc=[0,0]
colours=["error","#ff0000","#00ff00","#ffff00","#fe98ff","#050056","#4afe80","#555555","#380001"]
Longitina =[]
Latina =[]
Alien =[]
clients = []
nicknames = []
Commandlist = []
#Commandlist[90,16384+160,295,90 ,16384+160,32768,49152,295,0,220+16484,32768,49152,205,270,16384+160,115,270,16384+160,32768,49152,115,180,16384+220,32768,49152,45,85+16384,180,340,90,16384+120,180,340,90,206,268+16384]
reachedpoint=False 
investigated=False
theory_loc=[]
test_loc=[]
sav_dist=0


# if negative ie backwards add 1000 to distance
#colours
#red 1
#green 2
#yellow 3
#pink 4
#darkblue 5
#light green 6


# restart = False
#
#make sure you add these to the angle and distance you get
# global Commandlist

# Create a TCP/IP socket

#rover = Rover  


# sav_dist=0
global Sock

           

def broadcast(message):
    
    try:
        client=clients[1] ##change when youre changing the client order
        message = message.to_bytes(2, byteorder = 'big', signed=False)
        client.send(message)

    except:
        client, address = Sock.accept()
        print("connected to " + str(address))
        nickname  = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

def handle(client,wid,):
    ##maybe import automate
    global angle
    global Commandlist
    global autogen
    global sav_dist
    global needmore
    global point
    global map
    global sav_loc
    global drawin
    global loc
    global dist
    global Longitina
    global Latina
    global Alien
    global colour
    global point
    global reachedpoint
    global investigated
    global aliens



    i = 0
    # sav_dist = 0
    # x=0
    # y=0
    # sav_loc =[x,y]
    
    while True:
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------")
        try:
            #Recieving message
            message = client.recv(wid)
            # if wid==2:
            #     print(message[0])
            #     print(message[1])
            # if wid ==5:
            #     print(message[1])
            #     print(message[2])
            #     print(message[3])
            #     print(message[4])
            
            #POS
            if message[0]==0:
                print("POS")
                top=message[1]<<8
                angle=top+message[2]
                if angle>32768:
                    angle= 32768-angle
                top=message[3]<<8
                dist=top+message[4]
                if dist>32768:
                    dist= 32768 - dist
                print("recieved")
                while angle > 360:
                    angle=angle-360
                while angle < 0:
                    angle = angle+360
                print(angle)
                print(dist)
                loc=yap.calc_loc(angle,sav_dist,dist,sav_loc)
                loc[0]=int(loc[0])
                loc[1]=int(loc[1])
                print("loc")
                print(loc)
                test_loc=loc
                drawin=1

                # if theory_angle== 0:
                #     theory_loc[1]=theory_loc[1]+10
                # elif theory_angle == 90:
                #     theory_loc[0]=theory_loc[0]+10
                # elif theory_angle == 180:
                #     theory_loc[1]=theory_loc[1]-10
                # elif theory_angle == 270:
                #     theory_loc[0]=theory_loc[0]-10
                # elif theory_angle== 45:
                #     theory_loc[0]=theory_loc[0]+8.509
                #     theory_loc[1]=theory_loc[1]+8.509
                # elif theory_angle == 135:
                #     theory_loc[0]=theory_loc[0]+8.509
                #     theory_loc[1]=theory_loc[1]-8.509
                # elif theory_angle == 225:
                #     theory_loc[0]=theory_loc[0]-8.509
                #     theory_loc[1]=theory_loc[1]-8.509
                # elif theory_angle == 270:
                #     theory_loc[0]=theory_loc[0]-8.509
                #     theory_loc[1]=theory_loc[1]+8.508             
                




            #UPM
            if message[0]==1:

                print("UPM")
                # print(len(Commandlist))
                needmore=1
                if len(Commandlist)==0:
                    if ((sav_loc[0] < automate.poi[point][0] + 3) and (sav_loc[0] > automate.poi[point][0]-3) and (sav_loc[1] < automate.poi[point][1] + 3) and (sav_loc[1] > automate.poi[point][1]-3)):
                        print("reachedpoint worked")
                        reachedpoint=True
                        investigated=False
                    else: #not in poi p
                        reachedpoint = False
                    if autogen == 1:
                        dalist=automate.exe(sav_loc,point, reachedpoint, investigated,map)
                        point=dalist[0]
                        Commandlist=dalist[1]
                        reachedpoint=dalist[2]
                time.sleep(1.5)

                    



            ##IDA
            if message[0]==2:
                print("IDA")
                investigated= False
                reachedpoint = False 
                print(message[1])
                print(message[2])
                print(message[3])
                print(message[4])
                top=message[1]<<8
                colour=top+message[2]
                top=message[3]<<8
                dist=top+message[4]
                if colour != 0:
                    
                    if colour ==9:
                        pass
                        
                    elif colour==8:
                        stripes=dist>>7
                        dist=dist&127
                        print("stripes")
                        print(stripes)
                        print("dist")
                        print(dist)
                        #deadzone+(2*stripes)+10
                    elif colour!=9:  
                        print("colour="+ str(colour))
                        print("dist="+str(dist))

                    # Commandlist.clear()
                    # dalist=automate.exe(sav_loc,point,reachedpoint, investigated,map)
                    # point=dalist[0]
                    # Commandlist=dalist[1]
                    # reachedpoint=dalist[2]
                    drawin=2
                    
                    
                #colour=8
                #fist 4 bits are (10,7) 7 shift
                #dist is the bottom 7 and with 127
                #
                
                    #make plot deadzone
                #automate.exe()
                
            #RAD    
            if message[0]==3:
                print("RAD")
                #make it plot the fan

            #Bat
            if message[0]==4:
                print("BAT")
                bat_level=message[4]
                print("batlevel")
                a_file = open("components/Level.js", "r")
                list_of_lines = a_file.readlines()
                list_of_lines[3] = "let inputval = "+ bat_level + ";" + "\n"
                a_file = open("components/Level.js", "w")
                
            #init
            if message[0]==5:
                print("init")
                if message[1]==1:
                    sav_loc=[20,20]
                    angle=90
                if message[1]==2:
                    sav_loc=[20,220]
                    angle=0
                if message[1]==3:
                    sav_loc=[340,20]
                    angle=180
                if message[1]==4:
                    sav_loc=[340,220]
                    angle=270 
                output = automate.update_start(map,sav_loc[0],sav_loc[1])
                investigated=False
                point=output[0]
                Commandlist=output[1]
                print(Commandlist[0])

            #MOV
            if message[0]==6:
                print("MOV")
                print(angle)
                print("is", message[1])
                if autogen==0:
                    if message[1]==1:
                        print("almost")
                        Commandlist.append(16394)########################
                        print(Commandlist)
                        print("up")
                    if message[1]==2:
                        Commandlist.append(16894)
                        print("back")
                        print(Commandlist)
                    if message[1]==3:
                        angletarget = angle-45
                        if angletarget < 0:
                            angletarget=angletarget+360
                            # theory_angle=theory_angle-45
                        if angletarget > 360:
                            angletarget=angletarget-360
                            # theory_angle=theory_angle+45
                        Commandlist.append(angletarget)
                        print (angletarget)
                        print("left")

                    if message[1]==4:  
                        angletarget=angle+45
                        if angletarget < 0:
                            angletarget=angletarget+360
                        if angletarget > 360:
                            angletarget=angletarget-360
                        Commandlist.append(angletarget)
                        print (angletarget)
                        print("right")

               

            #autoswitch
            if message[0]==7:
                print("auto/man switch")
                Commandlist.clear()
                if message[1]==1: #manual
                 
                    autogen=0
                if message[1]==2: #auto
                  
                    autogen=1
                    # dalist=automate.exe(sav_loc, point, reachedpoint, investigated)
                    # point=dalist[0]
                    # Commandlist=dalist[1]
                    # print(Commandlist[0])
                    # reachedpoint=dalist[2]
                    # print(Commandlist)

            #radar switch            
            if message[0]==8:
                print("radar switch")
                if message[2]==1:
                    alines=1
                if message[2]==2:
                    aliens=1
                msg=msg<<8
                broadcast(msg)


            print("needmore")
            print(needmore)
            #waiting for command clause
            if needmore == 1:
                print("needmore")
                if len(Commandlist)>0:
                    needmore=0
                    command=Commandlist[0]
####################### update when connected to rover ######################################################
                    
                    #broadcast(Commandlist[0])
                    Commandlist.pop(0)
                    ##################if dont send anymore this is ya boi#########################################
                    broadcast(command)
                    print(command)
                    print(len(Commandlist))

                else:
                    print("in commandlist 0")
                    if ((sav_loc[0] < automate.poi[point][0] + 3) and (sav_loc[0] > automate.poi[point][0]-3) and (sav_loc[1] < automate.poi[point][1] + 3) and (sav_loc[1] > automate.poi[point][1]-3)):
                        reachedpoint=True
                        investigated=False
                    else: 
                        reachedpoint = False
                    if autogen == 1:
                        delist= automate.exe(sav_loc,point, reachedpoint, investigated,map)
                        point=delist[0]
                        Commandlist=delist[1]
                        reachedpoint=delist[2]
                        print(Commandlist)

        except:
            print("dumbass check ur code")       
            

def receive(n):
    number_of_devices = 0
    while number_of_devices < n:
        port_number =16000-(number_of_devices*1000)
        print(port_number)
        # Create a TCP/IP socket
        
        Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # Bind the socket to the port
        server_address = ('192.168.43.192', port_number)
        # print('starting up on port ' + server_address[0] + server_address[1])
        Sock.bind(server_address)
        # Accept Connection
        print("looking for new connection")
        Sock.listen(1)
        client, address = Sock.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        # client.send("N".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)

        if port_number==15000:
            wid = 5
            
        if port_number==16000:
            wid=2
            
            # Start Handling Thread For Client
        number_of_devices+=1
        print("started thread with new device with name", nickname)
        thread = threading.Thread(target=handle, args=(client,wid,))
        thread.start()
#end

#automate.update_start(0,0,0)
print("input num of expected devices")
# print("Sock is listening on "+str(server_address[0])+":"+str(server_address[1])#
#make brders around arena map:
automate.make_border(map)

    ###bored hear####

##Splitting Commandlist
def SplitCommand(Commandlist):
    new_Commandlist = []
    for x in Commandlist:
        y = x
        while y > (16444):
            new_Commandlist.append(60)
            y = y - 60
        new_Commandlist.append(y)
    return new_Commandlist

    


number_of_devices=2
receive(number_of_devices)
while True:
    if drawin==1:
        yap.alien(loc[0],loc[1],angle,"#ffffff",dist,Longitina,Latina,Alien)
        drawin=0
    elif drawin==2:
        print("beta detected, opinion rejected")
        print(Longitina)
        print(Latina)
        print(colour)
        yap.alien(sav_loc[0],sav_loc[1],angle,colours[colour],dist,Longitina,Latina,Alien)
        drawin=0
    elif aliens == 1:
        print("beta detected, opinion rejected")
        yap.alien(sav_loc[0],sav_loc[1],angle,colours[colour],dist,Longitina,Latina,Alien)
        i=0
        print("--------------------------------------------------------------")
        for i in len(Longitina):
            print(Longitina[i])
        i=0
        print("--------------------------------------------------------------")
        for i in len(Longitina):
            print(Latina[i])
        i=0
        print("--------------------------------------------------------------")
        for i in len(Longitina):
            print(colour[i])
        print("--------------------------------------------------------------")
        
        aliens=0






# if negative ie backwards add 1000 to distance

#colours
#red 1
#green 2
#yellow 3
#pink 4
#darkblue 5
#light green 6