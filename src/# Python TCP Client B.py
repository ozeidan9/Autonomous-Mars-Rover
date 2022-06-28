# Python TCP Client B
import socket 

host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000 
MESSAGE = "noob"
 
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientB.connect((host, port))

while MESSAGE != 'exit':
    MESSAGE=MESSAGE.encode("ascii")
    tcpClientB.send(MESSAGE)     
    data = tcpClientB.recv(BUFFER_SIZE)
    MESSAGE=data.decode("ascii")
    print (" Client1 received data:", data)

tcpClientB.close() 