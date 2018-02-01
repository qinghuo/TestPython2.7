#-- coding:utf-8 --
import socket

host="127.0.0.1"
port=9999
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
client.send(b"OPTIONS * HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n")
reponse=client.recv(4096)
print(reponse)
