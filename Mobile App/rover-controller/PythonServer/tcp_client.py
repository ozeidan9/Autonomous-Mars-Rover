import socket

TCP_IP = '10.214.130.102'
TCP_PORT = 15850
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT))
print('begun')

msg = 'Hello server'
s.send(msg.encode())

data = s.recv(BUFFER_SIZE)
print ('received data: ', data)

s.close()



