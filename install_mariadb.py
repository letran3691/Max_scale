import os,subprocess,time,fileinput


server1_ = os.popen("ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\\2/p'").read().split('\n')
server1 = server1_[0]
host = subprocess.check_output('cat /etc/hostname',shell=True,universal_newlines=True)
host_n1 =host.rstrip('\n')


server2 = input('Enter ip server2: ')
host_n2 = input('Enter hostname server2:')

server3 = input('\nEnter ip server3: ')
host_n3 = input('Enter hostname server3:')

####config file hosts
with open('/etc/hosts','a+') as f:

   f.write('\n'+ server1 +' '+ host_n1)
   f.write('\n'+ server2 +' '+ host_n2)
   f.write('\n'+ server3 +' '+ host_n3)
   f.close()

#####transfer file hosts to servers
os.system('scp root@'+server2+':/etc/')
os.system('scp root@'+server3+':/etc/')


###### install mariadb

os.system('curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash')
os.system('yum -y install MariaDB-server')
os.system('mysql_secure_installation')

print('install server1 done!!!\n')
time.sleep(3)
os.system('ssh root@'+server2+ 'curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash ; yum -y install MariaDB-server;  mysql_secure_installation')
print('install server2 done!!!\n')
time.sleep(3)

os.system('ssh root@'+server3+ 'curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash ; yum -y install MariaDB-server;  mysql_secure_installation')
print('install server3 done!!!\n')
time.sleep(3)

#### config wsrep_cluster
with fileinput.FileInput('server.cnf', inplace=True,backup='.bak') as  f2:
    for line in f2:
       print(line.replace('wsrep_cluster_address=gcomm://','wsrep_cluster_address=gcomm://'+server1+','+server2+','+server3),end='')
    f2.close()

####### transfer file config wsrep_cluster to servers
os.system('scp /root/Max_scale/server.cnf root@'+server2+':/etc/my.cnf.d/')
os.system('scp /root/Max_scale/server.cnf root@'+server3+'://etc/my.cnf.d/')

print('start cluster on server1\n')
time.sleep(3)
os.system('galera_new_cluster')
inf = os.popen('ps -f -u mysql | more').read()

print('\ninfo cluster'+inf)

time.sleep(4)

os.system("mysql -uroot -p -e \"show status like '%wsrep_cluster_size%';\"")


############ start mariadb on servers
os.system(' ssh root@'+server2+ ' systemctl start mariadb.service; systemctl enable mariadb.service')

os.system(' ssh root@'+server3+ ' systemctl start mariadb.service; systemctl enable mariadb.service')

print('show info wsrep_cluster_size\n')
time.sleep(3)
os.system("mysql -uroot -p -e \"show status like '%wsrep_cluster_size%';\"")

print('show more info wsrep\n')
os.system("mysql -uroot -p -e \"show status like 'wsrep%'\"")

print('\nConfig done!!!!!!!')



