import socket
import sys


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('localhost', 15000)
# print('starting up on port ' + server_address[0] + server_address[1])
sock.bind(server_address)


# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()


    try:
        print('connection ')

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            data = data.decode()
            print(data)

            opcode = data[0:3]
            level_val = data[3:6]

            print(opcode)
            print(level_val)



            if opcode == 'BAT':
                print('recieved battery level')
                
                infile = open('components/Level.js','r+')
                content = infile.readlines() #reads line by line and out puts a list of each line
                content[3] = 'let inputval = ' + level_val + ';' #replaces content of the 2nd line (index 1)
                # infile.write(''.join(content))
                infile.close()
                infile = open('components/Level.js', 'w') #clears content of file. 
                infile.close
                infile = open('components/Level.js', 'r+')
                for item in content: #rewrites file content from list 
                    infile.write("%s" % item)
                infile.close()

                
                
                # connection.sendall('data')


            else:
                print('no more data')
                break
            
    finally:
        # Clean up the connection
        connection.close()

