#!/usr/bin/python3.6

import os,time,subprocess,fileinput,sys


print('Disable firewalld\n')

os.system('systemctl stop firewalld')
os.system('systemctl disable firewalld')


with fileinput.FileInput('/etc/selinux/sql', inplace=True,backup='.bak') as  f1:

    for line in f1:
       print(line.replace('SELINUX=enforcing','SELINUX=disabled'),end='')
    f1.close()


############################################################################### install mariadb
print('\nBegin install Mariadb\n')
time.sleep(2)
os.system('curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash')
os.system('yum -y install MariaDB-server')
os.system('systemctl start mariadb.service')
os.system('systemctl enable mariadb.service')
print('\nConfig password root sql\n')
time.sleep(2)
os.system('mysql_secure_installation')
os.system('systemctl stop mariadb.service')

###############################################################################

print('\nSet hostname server.')

hostn = input('\nEnter hostname server: ')

with open("/etc/hostname",'w') as f:
    f.write(hostn)
    f.close()

############################################################################### get gateway

gw = os.popen("ip route |grep default | awk '{print $3}'").read()

############################################################################### get ip

ip_ = os.popen("ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\\2/p'").read().split('\n')
ip_server = ip_[0]

############################################################################### get netmask

net = os.popen("ip -o -f inet addr show | awk '/scope global/{sub(/[^.]+\//,\"0/\",$4);print $4}'").read().split('\n')
net_ = net[0]
netmask = net_.split('/')[-1]

################################################################################ list interfaces

inf_ = os.popen('ls /sys/class/net/').read().split()

print('\nConfig network')
time.sleep(2)

print('\nYour interfaces: '+str(inf_)+'\n')

inf = (inf_[0])

################################################################################# sql network interface
n = ''

while n != 'c':
    print('\n+ {:-<6} + {:-^15} + '.format('',''))
    print('| {:<20} | '.format('please enter your option'.title()))
    print('| {:<24} | '.format('[1]enter 1 default '))
    print('| {:<25} | '.format('[2]enter 2 to modify '))
    print('| {:<25} | '.format('[c]enter C to reboot '))
    print('+ {:-<6} + {:-^15} + '.format('',''))
    n = input('\nEnter option: '.title())

    if n == '1':

        with fileinput.FileInput('/etc/sysconfig/network-scripts/ifcfg-'+inf, inplace=True) as  f:
            for line in f:
                print(line.replace('BOOTPROTO="dhcp"','BOOTPROTO=static'),end='')
            f.close()

        with open('/etc/sysconfig/network-scripts/ifcfg-'+inf, 'a+') as f1:
            f1.write('\nIPADDR=' + ip_server)
            f1.write('\nFREFIX=' + netmask)
            f1.write('\nGATEWAY=' + gw)
            f1.write('\nDNS1='+ gw)
            f1.write('\nDNS2=8.8.8.8')
            f1.close()
        os.system('systemctl restart network')
        print('\nConfig network done!!! Plz hit C to reboot server'.title())


    elif n == '2':

        name_inf = input('Enter name inteface: ')
        ip = input('Enter ip your server: ')
        print('Example Enter Netmask: 8 16 24')
        netmask = input('Enter Netmask: ')

        with fileinput.FileInput('/etc/sysconfig/network-scripts/ifcfg-'+name_inf, inplace=True) as  f:
            for line in f:
                print(line.replace('BOOTPROTO="dhcp"','BOOTPROTO=static'),end='')
            f.close()

        with open('/etc/sysconfig/network-scripts/ifcfg-'+name_inf, 'a+') as f1:
            f1.write('\nIPADDR=' + ip)
            f1.write('\nFREFIX=' + netmask)
            f1.write('\nGATEWAY=' + gw)
            f1.write('\nDNS1='+ gw)
            f1.write('\nDNS2=8.8.8.8')
            f1.close()
        os.system('systemctl restart network')
        print('\nConfig network done!!! Plz hit C to reboot server'.title())

    elif n == 'c':
        print('reboot after 3s')
        time.sleep(3)
        os.system('reboot')

    else:
        print("\n\ti don't know your option!!!,".title(),'Please enter try!!!'.upper())



