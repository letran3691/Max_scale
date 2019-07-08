#!/usr/bin/env python3.6

import os,sys,time,fileinput

print('Disable firewalld\n')

os.system('systemctl stop firewalld')
os.system('systemctl disable firewalld')


with fileinput.FileInput('/etc/selinux/config', inplace=True,backup='.bak') as  f1:

    for line in f1:
       print(line.replace('SELINUX=enforcing','SELINUX=disabled'),end='')
    f1.close()


############################################################################# get ip

ip_ = os.popen("ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\\2/p'").read().split('\n')
ip_server = ip_[0]


############################################################################## get netmask

net = os.popen("ip -o -f inet addr show | awk '/scope global/{sub(/[^.]+\//,\"0/\",$4);print $4}'").read().split('\n')
net_ = net[0]
netmask = net_.split('/')[-1]

################################################################################ list interfaces

inf_ = os.popen('ls /sys/class/net/').read().split()

print('\nYour interfaces: '+str(inf_)+'\n')

inf = (inf_[0])


############################################################################### get gateway

gw = os.popen("ip route |grep default | awk '{print $3}'").read()

print('Config network.')
time.sleep(2)

n = ''

while n != 'c':
    print('\n+ {:-<6} + {:-^15} + '.format('',''))
    print('| {:<20} | '.format('please enter your option'.title()))
    print('| {:<24} | '.format('[1]enter 1 default '))
    print('| {:<25} | '.format('[2]enter 2 to modify '))
    print('| {:<25} | '.format('[c]enter C to continue '))
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
        print('Config network done!!! Plz hit C to continue'.title())


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
        print('Config network done!!! Plz hit C to continue'.title())

    elif n == 'c':
        break

    else:
        print("\n\ti don't know your option!!!,".title(),'Please enter try!!!'.upper())

############################################################################ Install && config Max_Scale

print('\nBegin install Maxscale and Mariadb-client\n')
os.system('curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash')
os.system('yum -y install maxscale MariaDB-client ')

os.system('cp /root/maxscale.cnf /etc/')

server1 = input('Enter ip server1: ')
server2 = input('Enter ip server2: ')
server3 = input('Enter ip server3: ')

user = input('Enter user cluster: ')
passw = input('Enter password user cluster: ')


print('edit file maxscale.cnf')
time.sleep(2)
with open('/etc/maxscale.cnf', 'r') as  f:
    newtext = f.read()

    while 'ddress=server1' in newtext:
        newtext=newtext.replace('ddress=server1','ddress='+server1)

    while 'ddress=server2' in newtext:
        newtext=newtext.replace('ddress=server2','ddress='+server2)

    while 'ddress=server3' in newtext:
        newtext =newtext.replace('ddress=server3','ddress='+server3)

    while 'user=myuser' in newtext:
        newtext =newtext.replace('user=myuser','user='+user)

    while 'passwd=mypwd' in newtext:
        newtext =newtext.replace('passwd=mypwd','passwd='+passw)


with open('/etc/maxscale.cnf', "w") as f:
    f.write(newtext)

print('start maxscale service ')

os.system('systemctl start maxscale.service')

os.system('systemctl enable maxscale.service')

print('\nConfig done!!!!')
time.sleep(2)

os.system('mysql -h ' +ip_server+ ' -u'+user+ ' -p'+passw)

