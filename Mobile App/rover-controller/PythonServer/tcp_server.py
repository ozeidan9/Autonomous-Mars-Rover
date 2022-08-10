import socket
# import SocketServer

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.214.130.102"
        self.port = 15855
        self.addr = (self.server, self.port)
        # self.client.bind(self.addr)

    def disconnect(self):
        #disconnects from server
        self.client.close()

    def send_data(self, data):
        received = self.client.recv(20)
        # print("received data: ", data)
        print(received.decode())

        print("sending data: ", data)
        self.client.send(data.encode())

    def receive_data(self):
        self.listen(1)
        received = self.client.recv(20)
        # print("received data: ", data)
        return received.decode()



# class Network(SocketServer.BaseRequestHandler):
#     """
#     The RequestHandler class for our server.

#     It is instantiated once per connection to the server, and must
#     override the handle() method to implement communication to the
#     client.
#     """

#     def handle(self):
#         # self.request is the TCP socket connected to the client
#         self.data = self.request.recv(1024).strip()
#         print("{} wrote:".format(self.client_address[0]))
#         print(self.data)
#         # just send back the same data, but upper-cased
#         self.request.sendall(self.data.upper())

# if __name__ == "__main__":
    
#     HOST, PORT = "localhost", 9999

#     # instantiate the server, and bind to localhost on port 9999
#     server = SocketServer.TCPServer((HOST, PORT), Network)

#     # activate the server
#     # this will keep running until Ctrl-C
#     server.serve_forever()