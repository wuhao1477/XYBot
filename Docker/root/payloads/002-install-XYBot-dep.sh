#!/usr/bin/env bash

# ...existing code...

# 设置时区为上海/北京
ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
echo 'Asia/Shanghai' >/etc/timezone

# ...existing code...
cd /home/app/XYBot || exit
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple