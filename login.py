#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	本脚本提前执行一次，用以保存登陆状态
#
############################################################
import os,sys
if not sys.version_info[0] == 3:
	print("当前脚本只能在python3.x下运行，请更换您的python版本！")
	sys.exit()
import api
import json

def main():
	root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	client = api.Client()
	username = input('请输入您的账号:')
	password = input('请输入您的密码:')
	cookies_file = os.path.join(root_path, username + ".cookies")
	chapter_file = os.path.join(root_path, "captcha.png")
	if client.login(username, password, chapter_file):
		#存储cookies
		client.save_cookies(cookies_file)
		#存储username
		config_path = os.path.join(root_path, 'username.config')
		json_content = {"username": username}
		f = open(config_path, 'w')
		f.write(json.dumps(json_content))
		f.close()
		#提示语
		client.get_account_info()
		print('欢迎您:', client.userdata['uname'])
		print('登陆状态已储存，您现在可以使用其他功能脚本啦')
	else:
		sys.exit()

if __name__ == '__main__':
	main()