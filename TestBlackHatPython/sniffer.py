#-- coding:utf-8 --
import socket
import  os
import time

host="localhost"

if os.name=="nt":
    socket_protocol=socket.IPPROTO_IP
else:
    socket_protocol=socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.setblocking(False)
sniffer.bind((host,0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

print "start listening!"


if os.name=='nt':
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_NO)
while True:
    try:
        print sniffer.recvfrom(65565)
    except socket.error,e:
        print "not ready"
    time.sleep(1)
if os.name=='nt':
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)

