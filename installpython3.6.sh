#!/usr/bin/env bash

echo 'install python3.x'

yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools

### installation required GCC
#echo 'installation required GCC'
#sleep 4
#yum install epel-release gcc openssl-devel bzip2-devel wget -y
#
### Download Python
#
#echo 'Download Python'
#
#sleep 4
#cd /usr/src
#wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
#
### Extract
#tar xzf Python-3.6.8.tgz
#
## make and install
#
#echo 'make and install'
#
#sleep 4
#cd Python-3.6.8
#./configure --enable-optimizations
#make altinstall
#
#rm -f /usr/src/Python-3.6.8.tgz

chmod -R +x /root/Max_scale/*.py
echo 'Install python on server 1 done!!!'

sleep 3

############## config server 2
echo 'Config on server 2.'
sleep 3
echo "Enter ip server 2: "
read server2
echo 'install python3.x on server2'
sleep 2
ssh root@$server2 'yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools'

echo 'Transfer install_mariadb.py to server 2'
scp  /root/Max_scale/install_mariadb.py root@$server2:/root/
echo 'Permissions install_mariadb.py'
ssh root@$server2 'chmod +x /root/install_mariadb.py'

echo 'Install python on server 2 done!!!'
sleep 3
################# config server 3

echo 'Config on server 3.'
sleep 3
echo "Enter ip server 3: "

read server3

echo 'install python3.x on server3'
sleep 3
ssh root@$server3 'yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools '

echo 'Transfer install_mariadb.py to server 3'

scp  /root/Max_scale/install_mariadb.py root@$server3:/root/

echo 'Permissions install_mariadb.py'

ssh root@$server3 'chmod +x /root/install_mariadb.py'

echo 'Install python on server 3 done!!!'
sleep 3
############## config server Max_scale

echo 'Config on Max_scale.'
sleep 3
echo "Enter ip Max_scale: "
read Max_scale
echo 'install python3.x on Max_scale'
ssh root@$Max_scale 'yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools'

echo 'Transfer config_MaxScale.py to Max_scale'
scp  /root/Max_scale/config_MaxScale.py root@$Max_scale:/root/
echo 'Transfer maxscale.cnfy to Max_scale'
scp  /root/Max_scale/maxscale.cnf root@$Max_scale:/root/
echo 'Permissions config_MaxScale.py'
ssh root@$Max_scale 'chmod +x /root/config_MaxScale.py'
ssh root@$Max_scale 'echo 'Max_scale' > /etc/hostname; reboot'

echo 'Install python on Max_scale done!!!'

sleep 3

echo 'install mariadb on server 1'
python3.6 /root/Max_scale/install_mariadb.py