#!/usr/bin/env python3.6

import os,sys,time,fileinput

print('Disable firewalld\n')

os.system('systemctl stop firewalld')
os.system('systemctl disable firewalld')


with fileinput.FileInput('/etc/selinux/config', inplace=True,backup='.bak') as  f1:

    for line in f1:
       print(line.replace('SELINUX=enforcing','SELINUX=disabled'),end='')
    f1.close()


os.system('curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash')
os.system('yum -y install maxscale MariaDB-client ')

os.system('cp /root/maxscale.cnf /etc/')

server1 = input('Enter ip server1: ')
server2 = input('Enter ip server2: ')
server3 = input('Enter ip server3: ')

user = input('Enter user cluster: ')
passw = input('Enter password user cluster: ')


print('exit file maxscale.cnf')
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

print('config done!!!!')
time.sleep(2)
print('check')
os.system("mysql -h " +server1+' -u'+user+' -p'+passw +" \"show variables like 'hostname';\"")