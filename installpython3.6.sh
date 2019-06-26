#!/usr/bin/bash

## installation required GCC
echo 'installation required GCC'
sleep 4
yum install gcc openssl-devel bzip2-devel wget -y

## Download Python

echo 'Download Python'

sleep 4
cd /usr/src
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz

## Extract
tar xzf Python-3.6.8.tgz

# make and install

echo 'make and install'

sleep 4
cd Python-3.6.8
./configure --enable-optimizations
make altinstall

rm -f /usr/src/Python-3.6.8.tgz

chmod -R +x /root/Max_scale/*.py

############## config server 2

echo "Enter ip server 2: "
read server2

ssh root@$server2 'yum install epel-release -y ; yum install python36 -y; yum install python36-devel -y; yum install python36-setuptools -y'

scp  /root/Max_scale/install_mariadb.py root@$server2:/root/

ssh root@$server2 'chmod +x /root/install_mariadb.py'

################# config server 3

echo "Enter ip server 3: "

read server3

ssh root@$server3 'yum install epel-release -y ; yum install python36 -y; yum install python36-devel -y; yum install python36-setuptools -y'

scp  /root/Max_scale/install_mariadb.py root@$server3:/root/

ssh root@$server3 'chmod +x /root/install_mariadb.py'

python3.6 install_mariadb.py