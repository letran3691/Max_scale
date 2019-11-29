import os,subprocess,time,fileinput

###################################################################### get ip server1

# server1_ = os.popen("ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\\2/p'").read().split('\n')
# server1 = server1_[0]
os.system("ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -N ''")

host = subprocess.check_output('cat /etc/hostname',shell=True,universal_newlines=True)
host_n1 =host.rstrip('\n')

server1 = input('\nEnter ip server1: ')
server2 = input('\nEnter ip server2: ')
host_n2 = input('Enter hostname server2: ')

server3 = input('\nEnter ip server3: ')
host_n3 = input('Enter hostname server3: ')

Max_scale = input('\nEnter ip Max_scale: ')

os.system("ssh - copy - id - i / root /.ssh / id_rsa.pub root@"+server2)
os.system("ssh - copy - id - i / root /.ssh / id_rsa.pub root@"+server3)
os.system("ssh - copy - id - i / root /.ssh / id_rsa.pub root@"+Max_scale)


########################################################################config file hosts
with open('/etc/hosts','a+') as f:

   f.write('\n'+ server1 +' '+ host_n1)
   f.write('\n'+ server2 +' '+ host_n2)
   f.write('\n'+ server3 +' '+ host_n3)
   f.close()

########################################################################transfer file hosts to servers

print('\nTransfer file hosts to server2')
print('\nEnter password root server2.')
time.sleep(2)
os.system('scp /etc/hosts root@'+server2+':/etc/')
os.system('scp /root/Max_scale/my.cnf root@'+server2+':/etc/')

print('\nTransfer file hosts to server3')
print('\nEnter password root server3.')
time.sleep(2)
os.system('scp /etc/hosts root@'+server3+':/etc/')
os.system('scp /root/Max_scale/my.cnf root@'+server3+':/etc/')


os.system('cp /root/Max_scale/server.cnf /etc/my.cnf.d/')
os.system('scp /root/Max_scale/my.cnf /etc/')


######################################################################## config wsrep_cluster
with fileinput.FileInput('/etc/my.cnf.d/server.cnf', inplace=True,backup='.bak') as  f2:
    for line in f2:
       print(line.replace('wsrep_cluster_address=gcomm://','wsrep_cluster_address=gcomm://'+server1+','+server2+','+server3),end='')
    f2.close()

######################################################################### transfer file config wsrep_cluster to servers
print('\nEnter password root server2.')
os.system('scp /etc/my.cnf.d/server.cnf root@'+server2+':/etc/my.cnf.d/')
###########################################################################
print('\nEnter password root server3.')
os.system('scp /etc/my.cnf.d/server.cnf root@'+server3+':/etc/my.cnf.d/')
##########################################################################
os.system('systemctl stop mariadb.service')
print('start cluster on server1\n')
time.sleep(3)
os.system(' systemctl stop mariadb ; pkill -9 mysqld ; galera_new_cluster')
inf = os.popen('ps -f -u mysql | more').read()
print('\ninfo cluster'+inf)
time.sleep(4)
p_root = input('\nEnter password root sql : ')
os.system("mysql -uroot -p"+p_root + " -e \"show status like '%wsrep_cluster_size%';\"")


########################################################################### start mariadb on servers
print('\nStart sql on server2.')
print('\nEnter password root server2.')
os.system(' ssh root@'+server2+ ' systemctl stop mariadb ; pkill -9 mysqld ; systemctl restart mariadb ; systemctl enable mariadb.service')


print('\nStart sql on server3.')
print('\nEnter password root server3.')
os.system(' ssh root@'+server3+ ' systemctl stop mariadb ; pkill -9 mysqld ; systemctl restart mariadb; systemctl enable mariadb.service')

print('show info wsrep_cluster_size\n')
time.sleep(3)
os.system("mysql -uroot -p"+p_root+ " -e \"show status like '%wsrep_cluster_size%';\"")

print('show more info wsrep\n')
os.system("mysql -uroot -p"+p_root+ " -e \"show status like 'wsrep%';\"")

print('\nConfig done!!!!!!!')

############################################################################### create user cluster


print('\nCreate user cluster')
time.sleep(3)
usern = input('\nEnter username: ')
passw = input('Enter password: ')

# print("mysql -uroot -p"+p_root+ " -e \"select user,host,password from mysql.user;\"") ##### debug

os.system("mysql -uroot -p"+p_root+ " -e \"create user"'\''+usern+'\''"@"'\''+Max_scale+'\''"identified by "'\'' +passw+'\''';\"')
os.system("mysql -uroot -p"+p_root+ " -e \"grant select on mysql.user to"'\''+usern+'\''"@"'\''+Max_scale+'\''';\"')
os.system("mysql -uroot -p"+p_root+ " -e  \"grant select on mysql.db to"'\''+usern+'\''"@"'\''+Max_scale+'\''';\"')
os.system("mysql -uroot -p"+p_root+ " -e \"grant select on mysql.tables_priv to"'\''+usern+'\''"@"'\''+Max_scale+'\''';\"')
os.system("mysql -uroot -p"+p_root+ " -e \"grant show databases on *.* to"'\''+usern+'\''"@"'\''+Max_scale+'\''';\"')

print('\nShow user')
time.sleep(2)
os.system("mysql -uroot -p"+p_root+ " -e \"select user,host,password from mysql.user;\"")

print('\nTest sync. Auto create a database name "Cluster_test" \n')
time.sleep(2)
os.system("mysql -uroot -p"+p_root+ " -e \"create database Cluster_test;\"")

print('\nCreate databases done!!!!')
print('\nShow database on server1.')
time.sleep(2)
os.system("mysql -uroot -p"+p_root+ " -e \"show databases;\"")

print('\nShow database on server2.')
print('\nEnter password root server2')
time.sleep(2)
os.system('ssh root@'+server2+ ' \'mysql -uroot -p'+p_root+ " -e \"show databases;\"\'")

print('\nShow database on server3.')
print('\nEnter password root server3')
time.sleep(2)
os.system('ssh root@'+server3+ ' \'mysql -uroot -p'+p_root+ " -e \"show databases;\"\'")

print('\nDelete database Cluster_test')
time.sleep(2)
os.system("mysql -uroot -p"+p_root+ " -e \"DROP DATABASE Cluster_test;\"")

print('\nDelete databes done!!!')
print('\nshow database again')
os.system("mysql -uroot -p"+p_root+ " -e \"show databases;\"")
print('\nConfig Cluster done'.upper())


## fix bug

### check join vào cluster. mysql -u root -p -e "SHOW STATUS LIKE 'wsrep_cluster_size'"
### Node sql nào bị tắt đầu tiên  thì bạn khởi động lại cuối cùng ( Cách check node nào off đầu tiên trong file /var/lib/mysql/grastate.dat trên tất cả các node xem trường seqno số nào lớn nhất thì đó là node tắt đầu tiên. Nếu tất cả đều là số âm thì set 1 node bất kì là 1 sau đó khởi động node vừa set là 1 đó đầu tiên.
### Trường hợp mất cluster k tự join vào được, stop mysql trên tất cả các node sau đó chạy lệnh galera_new_cluster trên node có seqno lớn nhất . Kiểm tra lại bằng lệnh mysql -u root -p -e "SHOW STATUS LIKE 'wsrep_cluster_size'"










