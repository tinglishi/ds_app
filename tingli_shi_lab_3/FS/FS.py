from flask import Flask, request, request, jsonify
from socket import *
import logging

app = Flask(__name__ )
logging.getLogger().setLevel(logging.DEBUG)

def fibonacci_calc(n):
    if n < 0:
        logging.warning("Number should be greater than 0")
    if n in {0, 1}:
        return n
    return fibonacci_calc(n - 1) + fibonacci_calc(n - 2)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if number: 
        return jsonify(fibonacci_calc(int(number))), 200
    else:
        return jsonify('Number is not provided'), 400

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = int(data.get('as_port'))

    if hostname and ip and as_ip and as_port:
        c_socket = socket(AF_INET, SOCK_DGRAM)        
        c_socket.sendto("TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(hostname,ip).encode(), (as_ip, as_port))
        msg, server_addr = c_socket.recvfrom(2048)
        c_socket.close()

        if msg.decode() == 'Success':
            return jsonify('Success'), 201
        else:
            return jsonify('Failed'), 500
    else:
       return jsonify('Missing parameters'), 400
    
app.run(host='0.0.0.0', port=9090, debug=True)