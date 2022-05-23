import socket
import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path


'''     Mars Rover - Command  
        EC2 Server script       '''

def main():

    server_name = '18.132.60.200'  # public ipv4 of ec2
    server_port = 12000                        
    #create a TCP client socket
    ec2_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind board 1 socket to port 11000
    ec2_client_socket.bind(('', 16090))  # Board 2: 16000

    print("Running UDP client for board 1...")
    #user presses button to join game
    # Add user/player to database
    msg = "board1"
    ec2_client_socket.sendto(str.encode(msg), (server_name, server_port))
    print("sent to server")