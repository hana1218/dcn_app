import requests
import json
import socket
from socket import *
from flask import Flask, request, Response
app = Flask(__name__)


@app.route('/')
def user():
    return 'User server(US)'

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    # Get params from request arguments
    hostname = request.args['hostname'] 
    fs_port = int(request.args['fs_port'])
    number = int(request.args['number'])
    as_ip = request.args['as_ip']
    as_port = int(request.args['as_port'])
    

    if(hostname == '' or fs_port == '' or number == '' or as_ip == '' or as_port == ''):
        return Response("404 Bad request", status = 400)
    else:

        us_socket = socket(AF_INET, SOCK_DGRAM)
        message = {'TYPE': 'A', 'NAME': hostname}
        us_socket.sendto(json.dumps(message).encode(), (as_ip, as_port))

        # Get response from AS for ip address of fibonacci server
        response, client_ip = us_socket.recvfrom(2048)
        fs_ip = response.decode()

        return Response(requests.get(f"http://{fs_ip}:{fs_port}/fibonacci", params={"number": number}).content, status = 200)
    

app.run(host='0.0.0.0',
        port=8080,
        debug=True)