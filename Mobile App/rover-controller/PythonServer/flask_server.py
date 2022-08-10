from flask import Flask, request, jsonify, redirect, url_for
from tcp_server import Network
import socket


target_host = "192.168.43.192"
target_port = 16000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let the client connect
client.connect((target_host, target_port))

app = Flask(__name__)


client.send(("Mob App").encode()) 
print("connected")

@app.route('/start', methods=['POST', 'GET'])
def start_coordinate():
    # handle the POST request
    content = request.get_json(force=True)
    print(content['start'])
    data = content['start']
    # msg=data.encode()
    message_int = int(data)
    message = message_int.to_bytes(2, byteorder = 'big', signed=False)
    client.send(message)


@app.route('/mode', methods=['POST','GET'])
def mode_result():
    # handle the POST request
    content = request.get_json(force=True)
    print(content['mode'])
    data = content['mode']
    message_int = int(data)
    message = message_int.to_bytes(2, byteorder = 'big', signed=False)
    client.send(message)


@app.route('/toggle', methods=['POST','GET'])
def toggle_result():
    # handle the POST request
    content = request.get_json(force=True)
    print(content['toggle'])
    data = content['toggle']
    message_int = int(data)
    message = message_int.to_bytes(2, byteorder = 'big', signed=False)
    client.send(message)



@app.route('/mov_ctrl', methods=['POST', 'GET'])
def direction_result():
    # handle the POST request
    content = request.get_json(force=True)
    print(content['direction'])
    data = content['direction']
    message_int = int(data)
    message = message_int.to_bytes(2, byteorder = 'big', signed=False)
    client.send(message)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True,host='192.168.43.50', port=11000, use_reloader=False, threaded=True)
    print("running")

