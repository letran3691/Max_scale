import os,subprocess,time,fileinput


server1 =""
server2 = input('Enter ip server2: ')
server3 = input('Enter ip server3: ')

# os.system('curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash')
# os.system('yum -y install MariaDB-server')
# os.system('mysql_secure_installation')

with fileinput.FileInput('server.cnf', inplace=True,backup='.bak') as  f2:
    for line in f2:
       print(line.replace('wsrep_cluster_address=gcomm://','wsrep_cluster_address=gcomm://'+server1+','+server2+','+server3),end='')
    f2.close()


