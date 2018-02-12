#-- coding:utf-8 --
import paramiko

def ssh_command(ip,user,passwd,command):
    client=paramiko.SSHClient()
    #自动添加主机名及主机密钥到本地HostKeys对象，并保存
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=user,password=passwd)
    ssh_session=client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return

if __name__ == '__main__':
    ssh_command('172.20.100.112','dev','weidai@1234','ls')