#-- coding:utf-8 --
import socket
import time
host="127.0.0.1"
port=9990
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
client.settimeout(2)
client.send(b"pwd")
reponse=client.recv(4096)
print(reponse)
