#!/usr/bin/bash

echo 'install python3.x'

yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools

chmod -R +x /root/Max_scale/config_mariadb.py
chmod -R +x /root/Max_scale/install_mariadb.py
echo $'\nInstall python on server 1 done!!!'

sleep 3

#################################################################################### config server 2
echo $'\nConfig on server 2.'
sleep 3
echo "Enter ip server 2: "
read server2
echo 'install python3.x on server2'
sleep 2
echo $'\nEnter password root server2.'

ssh root@$server2 'yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools'

####################################################################################

echo $'\nTransfer install_mariadb.py to server 2'
echo $'\nEnter password root server2.'
scp  /root/Max_scale/install_mariadb.py root@$server2:/root/

#####################################################################################

echo $'\nPermissions install_mariadb.py'
echo $'\nEnter password root server2.'
ssh root@$server2 'chmod +x /root/install_mariadb.py'

echo $'\nInstall python on server 2 done!!!'
sleep 3
####################################################################################### config server 3

echo $'\nConfig on server 3.'
sleep 3
echo 'Enter ip server 3: '
read server3

echo $'\ninstall python3.x on server3'
sleep 3
echo $'\nEnter password root server3.'
ssh root@$server3 'yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools '

##################################################################################

echo $'\nTransfer install_mariadb.py to server 3'
echo $'\nEnter password root server3.'
scp  /root/Max_scale/install_mariadb.py root@$server3:/root/

#####################################################################################

echo $'\nPermissions install_mariadb.py'
echo $'\nnEnter password root server3.'
ssh root@$server3 'chmod +x /root/install_mariadb.py'
echo $'\nInstall python on server 3 done!!!'
sleep 3
###################################################################################### config server Max_scale

echo $'\ninstall python3.x on Max_scale.'
sleep 3
echo 'Enter ip Max_scale: '
read Max_scale
echo $'\ninstall python3.x on Max_scale'
echo $'\nEnter password root Max_scale.'
ssh root@$Max_scale 'yum install -y epel-release; yum install -y python36 python36-devel python36-setuptools'

######################################################################################

echo $'\nTransfer config_MaxScale.py to Max_scale'
echo $'\nEnter password root Max_scale.'
scp  /root/Max_scale/config_MaxScale.py root@$Max_scale:/root/

#########################################################################################

echo $'\nTransfer maxscale.cnfy to Max_scale'
echo $'\nnEnter password root Max_scale.'
scp  /root/Max_scale/maxscale.cnf root@$Max_scale:/root/

####################################################################################

echo $'\nPermissions config_MaxScale.py'
echo $'\nEnter password root Max_scale.'
ssh root@$Max_scale 'chmod +x /root/config_MaxScale.py'

######################################################################################
echo $'\nChange hostname and reboot Max_scale.'
echo $'\nEnter password root Max_scale.'
ssh root@$Max_scale 'echo 'Max_scale' > /etc/hostname; reboot'
echo $'\nInstall python on Max_scale done!!!'
sleep 3

######################################################################################


echo $'\ninstall mariadb on server 1'
python3.6 /root/Max_scale/install_mariadb.py