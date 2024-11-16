#!/usr/bin/env bash

cd /home/app || exit
git clone https://github.com/wuhao1477/xybot.git XYBot
cd XYBot || exit
# 删除以下行或修改为实际存在的分支
# git checkout dev