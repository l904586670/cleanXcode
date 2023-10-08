#!/bin/sh
# 用于检测项目中垃圾代码

if [ `command -v periphery` ];
then
    echo 'periphery 已经安装'
else
    brew install peripheryapp/periphery/periphery
fi

cd "`dirname \"$0\"`"
cd ../
periphery scan --workspace BudGlobal.xcworkspace --schemes BudGlobal-Alpha --targets BudGlobal
