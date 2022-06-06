
from re import X
import socket
# First import time module.
import time

level = 100
x=1
target_host = "localhost"
target_port = 16000
# create a socket connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let the client connect
client.connect((target_host, target_port))
# send some data

level="IDA010024000ff00ff0452828"
print(len(level))    
msg=level.encode()
time.sleep(1)
client.send(msg)
# level="IDA000000045ff00000002828"
# print(len(level))    
# msg=level.encode()
# client.send(msg)
# time.sleep(1)
# level="IDA0000000000000ff0003000"
# print(len(level))    
# msg=level.encode()
# client.send(msg)
# level="IDA-50-500450000000004242"
# print(len(level))    
# msg=level.encode()
# client.send(msg)
# time.sleep(1)
# level="IDA-50+501350000000004242"
# print(len(level))    
# msg=level.encode()
# client.send(msg)
# time.sleep(1)
# level="IDA+50+502250000000004242"
# print(len(level))    
# msg=level.encode()
# client.send(msg)
# time.sleep(1)
# level="IDA+50-503150000000004242"
# print(len(level))    
# msg=level.encode()
# client.send(msg)

for i in range (20):
    x=str((-i*3)-10)
    y=str((-i*3)-10) 
    level="POS"+x+y+"225"
    print (level)    
    msg=level.encode()
    client.send(msg)
    time.sleep(1)


#  x=(contr_data[3:6])
#                 y=(contr_data[6:9])
#                 Aangle=(contr_data[9:12])
#                 colour='#'+contr_data[12:18]
#                 dist=(contr_data[18:22])
#                 Rangle=int(contr_data[22:25])