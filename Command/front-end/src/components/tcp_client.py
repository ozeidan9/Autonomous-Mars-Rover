from re import X
import socket

level = 100

x=1

target_host = "localhost"

target_port = 15000

# create a socket connection

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# let the client connect

client.connect((target_host, target_port))

# send some data

while x !=0:

    level = input()

    msg=level.encode()

    client.send(msg)