import socket




target_host = "192.168.43.192"
target_port = 15000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let the client connect
client.connect((target_host, target_port))
message="rover"
message = message.encode("ascii")
client.send(message)
while True:
    message=0
    print("input command")
    command=input()
    if command=="":
        command ="POS"
    # message_int = int(data)
    # message = mPOessage_int.to_bytes(2, byteorder = 'big', signed=False)
    # client.send(message)
    if command == "UPM":
        message= message+4294967296
        message = message.to_bytes(5, byteorder = 'big', signed=False)
        client.send(message)
    if command == "POS":
        
        print("input x")
        x=input()
        x=int(x)
        print("input y")
        y=input()
        y=int(y)
        message=x<<16
        
        message=message+y
        print (message)
        message = message.to_bytes(5, byteorder = 'big', signed=False)
        client.send(message)
    if command == "IDA":
        code=2
        code=code<<32
        print(code)
        print("input colour")
        x=input()
        x=int(x)
        print("input distance")
        y=input()
        y=int(y)
        message=x<<16
        message=message+y+code
        print (message)
        message = message.to_bytes(5, byteorder = 'big', signed=False)
        client.send(message)
    if command =="BAT":
        print("input bat level")
        y=100
        message=message+y
        print (message)
        message = message.to_bytes(5, byteorder = 'big', signed=False)
        client.send(message)
        y=y-10
        
    
        

        
