from flask import Flask, request, jsonify
from socket import *
import requests

app = Flask(__name__ )

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port'))
    if hostname and fs_port and as_ip and as_port and number:
        client_socket = socket(AF_INET, SOCK_DGRAM)
        client_socket.sendto("TYPE=A\nNAME={}".format(hostname).encode(), (as_ip, as_port))
        msg, addr = client_socket.recvfrom(2048)
        client_socket.close()
        value = msg.decode().split('\n')[2].split('=')[1]
    
        r = requests.get("http://{}:{}/fibonacci?number= {}".format(value, fs_port, number))
        return jsonify(r.json()), 200
    else:
        return jsonify("Missing parameters"), 400

app.run(host='0.0.0.0',port=8080,debug=True)