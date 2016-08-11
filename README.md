#play with bilibili
##简介
* 模拟登陆bilibili弹幕网进行各类操作
* 哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili
##安装说明
* 需要在python3环境下运行
* 需要安装以下库
  	sudo pip3 install bs4
  	sudo pip3 install requests
  	sudo pip3 install pycrypto
  	sudo pip3 install rsa

##使用说明
####api.py
* 该脚本封装了一些bilibli常用api
* 该脚本无法直接运行，仅供其他脚本调用
####login.py
* 该脚本需要提前执行一次，之后才可运行其他脚本
* 该脚本会进行登录操作并保存cookies和登录状态
####handle_update.py
* 该脚本主要用于监听番剧更新并抢沙发
* 脚本用法请参见脚本顶部介绍
* 建议加入定时任务中运行

##短期内计划实现功能
* 自动监听番剧更新(完成)
* 自动抢沙发(完成)
* 登录验证码的识别(放弃，求大神实现后PR)