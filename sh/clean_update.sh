#!/bin/bash
# 若提示无执行权限，执行命令 chmod +x ./xxx.sh 

sudo apt-get autoclean # 清理旧版本的软件缓存 
sudo apt-get autoremove # 删除系统不再使用的孤立软件 
#sudo apt-get clean # 清理所有软件缓存 
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P # 清除残余的配置文件保证干净
sudo apt-get update && sudo apt-get upgrade # 升级
#sudo rm -rf /var/cache/apt/archives # apt-get install命令安装包下载路径 