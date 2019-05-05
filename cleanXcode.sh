#!/bin/bash
#--------------------------------------------
# author：小小强
#--------------------------------------------
echo "========开始清除Xcode========"
echo 
read -p "Are you sure? [yes/NO] " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
echo 
    exit 1
fi
echo 
echo "开始清除DerivedData..."
rm -rf ~/Library/Developer/Xcode/DerivedData
echo "DerivedData已清除"
echo 
read -p "是否要删除Archives，Xcode打包文件 [yes/NO] " -n 1 -r
if [[  $REPLY =~ ^[Yy]$ ]]
then
echo 
echo "开始清除Archives..."
rm -rf ~/Library/Developer/Xcode/Archives
echo "Archives已清除"
fi
echo 
read -p "是否要删除运行xcode后在模拟器上安装的app?⚠️⚠️⚠️ 此文件夹删除后需要重启Xcode [yes/NO] " -n 1 -r
if [[  $REPLY =~ ^[Yy]$ ]]
then
echo 
echo "开始清除运行xcode后在模拟器上安装的app..."
rm -rf ~/Library/Developer/CoreSimulator/Devices
echo "模拟器上安装的app已清除"
echo "CoreSimulator文件夹删除后请重启Xcode"
fi
echo ""

