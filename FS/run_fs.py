import requests
import json
import socket
from socket import *
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def f():
    return 'Fibonacci Server(FS)'

def fib(number):
    if number == 0:
        return 0
    elif number == 1 or number ==2:
        return 1
    else:
        return fib(number - 1) + fib(number - 2)

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    number = int(request.args.get['number'])
    return str(fib(number))

@app.route('/register', methods=['PUT'])
def register():

    hostname = request.json["hostname"]
    fs_ip = request.json["fs_ip"]
    as_ip = request.json["as_ip"]
    as_port = request.json["as_port"]

    # DNS registration
    us_socket = socket(AF_INET, SOCK_DGRAM) 
    message = json.dumps({'TYPE':'A', 'NAME':hostname, 'VALUE': fs_ip, 'TTL': 10 })
    us_socket.sendto(message.encode(), (as_ip, as_port))
    response, _ = us_socket.recvfrom(2048) 
    return message.decode()

app.run(host='0.0.0.0',
        port=9090,
        debug=True)