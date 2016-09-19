# play with bilibili
## 简介
* 模拟登陆bilibili弹幕网进行各类操作
* 哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili

## 安装说明
* 需要在python3环境下运行
* 需要安装以下库

```shell
sudo pip3 install bs4
sudo pip3 install requests
sudo pip3 install pycrypto
sudo pip3 install rsa
```

## 使用说明
* 首次运行请执行一次login.py，该脚本会进行登录操作并保存cookies和登录状态
* 之后运行grab_sofa.py，带GUI的监听番剧更新并抢沙发脚本

## grab_sofa.py解析
* 原理也就是在番剧的预计更新时间时开始刷新，直到刷到有更新或者超过最大次数判定为停更~
* 尝试使用了MVC模式来写，代码感觉稍微清晰一些，如果有任何槽点，请轻喷( ゜- ゜)

## 计划实现功能（二期）
* 自动点赞他人评论的功能
* 自动回复他人评论的功能
* bilibili注册答题器

## 计划实现功能（一期）
* 自动监听番剧更新(完成)
* 自动抢沙发(完成)
* ~~登录验证码的识别(放弃，求大神实现后PR)~~
* 通过直播登陆接口绕过了验证码

本项目同时托管在[Github.com](https://github.com/ookcode/BilibiliSofaSitter)与[Coding.net](https://coding.net/u/ookcode/p/bilibili/git)中