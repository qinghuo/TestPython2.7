#-- coding:utf-8 --
import socket
import  os
import ctypes


class FLAGS(object):
  # linux/if_ether.h

  ETH_P_ALL     = 0x0003 # 所有协议

  ETH_P_IP      = 0x0800 # 只处理IP层

  # linux/if.h，混杂模式

  IFF_PROMISC   = 0x100

  # linux/sockios.h

  SIOCGIFFLAGS  = 0x8913 # 获取标记值

  SIOCSIFFLAGS  = 0x8914 # 设置标记值



class ifreq(ctypes.Structure):

    _fields_ = [("ifr_ifrn", ctypes.c_char * 16),

                ("ifr_flags", ctypes.c_short)]
host="localhost"

import fcntl
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
ifr = ifreq()
ifr.ifr_ifrn = b'en5' #此处注意，这里写死了网卡名称，需要根据实际情况修改或者传入
fcntl.ioctl(s, FLAGS.SIOCGIFFLAGS, ifr) # 获取标记字段的名称
ifr.ifr_flags |= FLAGS.IFF_PROMISC # 添加混杂模式的值
fcntl.ioctl(s, FLAGS.SIOCSIFFLAGS, ifr) # 更新
s.bind((host,0))
s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
print s.recvfrom(65565)


