import socket
import threading
import sys
import yap
import time

Longitina =[]
Latina =[]
Alien =[]
n=1
# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('192.168.43.192', 15000)
# print('starting up on port ' + server_address[0] + server_address[1])
server.bind(server_address)


# Listen for incoming connections
server.listen(1)
connection1, client_address1 = server.accept() #connect controller first
connection2, client_address2 = server.accept()

print("Server is listening on "+str(connection)+":"+str(client_address[1]))

while True:
    # Wait for a connection
    print ('waiting for a connection')
    try:
        data = connection.recv(48)
        data=data.decode("ascii")
        print("data received: ", data)
#try cinvertuing above into try and except statements?

    
     

        

    except:
        print("no")
            # contr_data = connection.recv(48)

            # contr_data = contr_data.decode()
            # print('contr data: ' + contr_data)


            # opcodecontr = contr_data[0:3]


            # if opcodecontr == 'POS':
            #     x=int(contr_data[3:6])
            #     # print(x)
            #     y=int(contr_data[6:9])
            #     #print(y)
            #     Rangle=int(contr_data[9:12])
            #     #print(Aangle)
            #     yap.alien(x,y,Rangle,'#ffffff',0,0,Longitina,Latina,Alien,n)


            # if opcodecontr == 'IDA':
            #     #level="IDA"+"010"+"024"+"045"+"ff00ff"+"001"+"28"+"28"+"1"
            #     x=int(contr_data[3:6])
            #     # print(x)
            #     y=int(contr_data[6:9])
            #     #print(y)
            #     Aangle=int(contr_data[9:12])
            #     #print(Aangle)
            #     colour='#'+contr_data[12:18]
            #     #print(colour)
            #     Rangle=int(contr_data[18:21])
            #     #print(Rangle)
            #     dist=int(contr_data[21:25])
            #     dist=float(dist/100)
            #     #print(dist)
            #     yap.alien(x,y,Rangle,colour,Aangle,dist,Longitina,Latina,Alien,n)
            #     #yap.draw(Longitina, Latina, Alien)
            #     #print(Longitina[0])
            #     # f = open("Command/src/components/Map.js", "a")
            #     # f.close()
            #     # f.close()



            # if opcodecontr == 'BAT':
                
            #     level_val = contr_data[3:6]

            #     print('recieved battery level')
                
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

            # if opcodecontr == 'MOV':
            #     movctrl=contr_data[3]





            # # else:
            #    #print('no more data')
            #      break
            

    time.sleep(1)