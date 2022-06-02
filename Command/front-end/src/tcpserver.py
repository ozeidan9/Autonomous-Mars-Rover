import socket
import sys


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('localhost', 16000)
# print('starting up on port ' + server_address[0] + server_address[1])
sock.bind(server_address)


# Listen for incoming connections
sock.listen(1)


while True:
    # Wait for a connection
    print ('waiting for a connection')
    
    connection_contr, client_address_contr = sock.accept() #connect controller first

    connection_mobapp, client_address_mobapp = sock.accept() #then! connect mobile app

#try cinvertuing above into try and except statements?

    try:
        print('connection ')

        while True:

            contr_data = connection_contr.recv(20)
            mobapp_data = connection_mobapp.recv(20)

            contr_data = contr_data.decode()
            print('contr data: ' + contr_data)

            app_data = app_data.decode()
            print('mobile app data: ' + app_data)


            opcodecontr = contr_data[0:3]

        


            if opcodecontr == 'BAT':
                
                level_val = contr_data[3:6]

                print('recieved battery level')
                
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

            
                # connection.sendall('data')
            
            if app_data:

                instr = app_data[3:4]
                print('recieved DIRECTION / MODE')

                msg=instr.encode()
                connection_mobapp.send(msg)


            else:
                print('no more data')
                # break
            
    finally:
        # Clean up the connection
        connection_contr.close()
        connection_mobapp.close()

