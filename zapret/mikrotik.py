import paramiko
import os

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

def add_addresslist(servers, ip_list):
    """ servers must be a dict, ip_list should be a list """
    for server, params in servers.iteritems():
        ssh.connect(server, port=params['port'], username=params['login'])

        # Flushing the previous address-list
        ssh.exec_command("/ip firewall address-list remove [/ip firewall address-list find list=zapret-info]")
         
        for ip in ip_list:
            ssh.exec_command("/ip firewall address-list add list=zapret-info address=%s" % ip)
        
        ssh.close()
