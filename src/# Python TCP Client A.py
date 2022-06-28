# Python TCP Client A
import socket 

host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000 
MESSAGE = "lol"
 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))

while MESSAGE != 'exit':
    MESSAGE=MESSAGE.encode("ascii")
    tcpClientA.send(MESSAGE)     
    data = tcpClientA.recv(BUFFER_SIZE)
    MESSAGE=data.decode("ascii")
    print (" Client2 received data:", data)


tcpClientA.close() 