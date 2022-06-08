from http import server
import socket
import threading
import yap

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 15000)
# print('starting up on port ' + server_address[0] + server_address[1])
server.bind(server_address)
# Listen for incoming connections
server.listen(1)

clients = []
nicknames = []


Longitina =[]
Latina =[]
Alien =[]
n=1



def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            print("in handle")
            message = client.recv(1024)
            message = message.decode("ascii")
            opcode = message[0:3]
            if opcode == "MOV" or "MOD":
                # broadcast(message)
                print(message)

            if opcode == "POS":
                x=int(message[3:6])
                # print(x)
                y=int(message[6:9])
                #print(y)
                Rangle=int(message[9:12])
                #print(Aangle)
                yap.alien(x,y,Rangle,'#ffffff',0,0,Longitina,Latina,Alien,n)
           
            if opcode == "IDA":
               #level="IDA"+"010"+"024"+"045"+"fF00ff"+"001"+"28"+"28"+"1"
                x=int(message[3:6])
                # print(x)
                y=int(message[6:9])
                #print(y)
                Aangle=int(message[9:12])
                #print(Aangle)
                colour='#'+message[12:18]
                #print(colour)
                Rangle=int(message[18:21])
                #print(Rangle)
                dist=int(message[21:25])
                dist=float(dist/100)
                #print(dist)
                yap.alien(x,y,Rangle,colour,Aangle,dist,Longitina,Latina,Alien,n)
                #yap.draw(Longitina, Latina, Alien)
                #print(Longitina[0])
                # f = open("Command/src/components/Map.js", "a")
                # f.close()
                # f.close()
            
            if opcode == 'BAT':
                
                level_val = message[3:6]

                print("recieved battery level")
                
                infile = open('components/Level.js','r+')
                content = infile.readlines() #reads line by line and out puts a list of each line
                content[3] = 'let inputval = ' + level_val + ';' #replaces content of the 2nd line (index 1)
                infile.close()
                infile = open('components/Level.js', 'w') #clears content of file. 
                infile.close
                infile = open('components/Level.js', 'r+')
                for item in content: #rewrites file content from list 
                    infile.write("%s" % item)
                infile.close()


        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            # broadcast((nickname + "left the chat!").encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print("connected to " + str(address))

        client.send('Nick'.encode('ascii'))
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