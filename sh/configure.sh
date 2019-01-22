#!/bin/bash
# 安装完Ubuntu16.04后进行系统配置
# 需要想更换清华源
# 若提示无执行权限，执行命令 chmod +x ./xxx.sh 

# 修改菜单栏位置
gsettings set com.canonical.Unity.Launcher launcher-position Bottom

# 修改系统时间
timedatectl set-local-rtc 1 --adjust-system-clock

# 禁用自动挂载U盘、硬盘等
gsettings set org.gnome.desktop.media-handling automount false
gsettings set org.gnome.desktop.media-handling automount-open false

# 删除无用软件
sudo apt-get --purge remove \
    unity-webapps-common \
    libreoffice-common \
    thunderbird \
    totem \
    rhythmbox \
    empathy \
    brasero \
    simple-scan \
    gnome-mahjongg \
    aisleriot \
    gnome-mines \
    cheese \
    transmission-common \
    gnome-orca \
    webbrowser-app \
    gnome-sudoku \
    onboard \
    deja-dup \
    firefox* \
    imagemagick-common \
    gedit

# 安装exFAt格式U盘软件
sudo apt-get install exfat-fuse

# 清理缓存
sudo apt-get autoclean   # 清理旧版本的软件缓存
sudo apt-get autoremove  # 删除系统不再使用的孤立软件
sudo apt-get clean       # 清理所有软件缓存