from socket import *
server_port = 53533

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
mappings = {}

while True:
    # Receive msg
    msg, addr = server_socket.recvfrom(2048)
    decoded_msg = msg.decode()
    if 'VALUE' in decoded_msg:
        splitted = decoded_msg.split('\n')
        name = splitted[1].split('=')[1]
        value = splitted[2].split('=')[1]
        mappings[name] = value
        server_socket.sendto("Success".encode(), addr)
    else: #QUERY
        name = decoded_msg.split('\n')[1].split('=')[1]
        if name in mappings:
            res = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(name, mappings[name])
            server_socket.sendto(res.encode(), addr)