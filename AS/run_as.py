import requests
import json
import socket
from socket import *


socket = socket(AF_INET, SOCK_DGRAM)
socket.bind(('', 53533))

while(True):

    msg, ip = socket.recvfrom(2048)
    message = json.loads(msg.decode())

    if len(message) == 4: 
        name, value, type, ttl = message
	    
        with open('record.txt', 'a') as f:
		    
            f.write("TYPE="+type+",NAME="+name+",VALUE="+value +",TTL="+ttl+"\n")
            msg = '201'
            
    elif len(message) == 2:  
        type, name = message
        file1 = open('record.txt', 'r')
		
        lines = file1.readlines()
		
        for line in lines:
			
            tmp = line.split(",")
			
            if tmp[1].split("=")[1] == name:
				
                msg = line
            else:
                msg = '400'
    else:
        msg ='400'

    socket.sendto(msg.encode(), ip)