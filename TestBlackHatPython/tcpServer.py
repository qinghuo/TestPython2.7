#-- coding:utf-8 --
import socket
import threading

bind_ip="127.0.0.1"
bind_port=9999
#AF_INET 说明使用的是ip4地址 SOCK_STREAM说明使用的协议是tcp
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)
print("[*] listening on %s:%d"%(bind_ip,bind_port))

def handle_client(client_socket):
    requst=client_socket.recv(1024)
    print("[*]received:%s"%requst)
    client_socket.send(b"ack")
    client_socket.close()

while True:
    client,addr=server.accept()
    print "[*] accepted connection from :%s:%d"%(addr[0],addr[1])
    client_handler=threading.Thread(target=handle_client,args=(client,))
    client_handler.start()


