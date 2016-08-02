#!/usr/bin/python3
#coding=utf-8
############################################################
#
# 哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili
#
# 需要在python3环境下运行
#
# 需要安装bs4库：sudo pip3 install bs4
#
# Created by Vincent on 16-7-21.
#
############################################################
import os,sys
if not sys.version_info[0] == 3:
	print("当前脚本只能在python3.x下运行，请更换您的python版本！")
	sys.exit()

import requests
import requests.utils
import pickle
import json
import rsa
import binascii
from bs4 import BeautifulSoup
import urllib

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5',
	'X-Requested-With': 'XMLHttpRequest',
	'Referer': 'http://www.bilibili.com',
}

class Client():
	def __init__(self):
		self.session = requests.Session()
		self.session.headers = headers
		self.userdata = ''

	#密码执行加密
	def _encrypt(self, password, token):
		password = str(token['hash'] + password).encode('utf-8')
		pub_key = token['key']
		pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
		message = rsa.encrypt(password, pub_key)
		message = binascii.b2a_base64(message)
		return message

	def load_cookies(self, path):
		with open(path, 'rb') as f:
			self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
			self.userdata = {}

	def save_cookies(self, path):
		with open(path, 'wb') as f:
			#cookiejar转为dict
			cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
			#写入文件
			pickle.dump(cookies_dic, f)

	def login(self, username, password, captcha_path):
		#访问登陆页面
		response = self.session.get('https://passport.bilibili.com/login')
		#请求验证码图片
		response = self.session.get('https://passport.bilibili.com/captcha')
		#保存验证码
		f = open(captcha_path,'wb')
		f.write(response.content)
		f.close()
		#获取加密的token
		response = self.session.get('http://passport.bilibili.com/login?act=getkey')
		token = json.loads(response.content.decode('utf-8'))
		#密码加密
		password = self._encrypt(password, token)
		captcha_code = input("请输入图片上的验证码：")
		#请求登陆
		preload = {
			'act': 'login',
			'gourl': '',
			'keeptime': '2592000',
			'userid': username,
			'pwd': password,
			'vdcode':captcha_code
		}
		response = self.session.post('https://passport.bilibili.com/login/dologin', data=preload)
		try:
			#解析返回的html，判断登陆成功与否
			soup = BeautifulSoup(response.text, "html.parser")
			center = soup.find('center').find('div')
			info = list(center.strings)[0]
			info = info.strip()
			print(info)
			return False
		except Exception as e:
			#登陆成功
			return True

	#获取个人信息
	def get_account_info(self):
		response = self.session.get('https://account.bilibili.com/home/userInfo')
		data = json.loads(response.content.decode('utf-8'))
		try:
			if data['status'] == True:
				self.userdata = data['data']
				return True
		except Exception as e:
			pass
		return False

	#获取个人通知消息个数
	def get_notify_count(self):
		#CaptchaKey
		response = self.session.get('http://www.bilibili.com/plus/widget/ajaxGetCaptchaKey.php?js')
		captcha = response.text.split('\"')[1]
		response = self.session.get('http://message.bilibili.com/api/notify/query.notify.count.do?captcha=' + captcha)
		print(response.text)

	#抢沙发
	def do_reply(self, avid, content):
		preload = {
			"jsonp":"jsonp",
			"message":content,
			"type":1, 
			"plat":1,
			"oid":avid
		}
		preload = urllib.parse.urlencode(preload) 
		response = self.session.post("http://api.bilibili.com/x/reply/add", data=preload)
		print(response.text)

def main():
	client = Client()
	username = input('请输入您的账号:')
	root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	cookies_file = os.path.join(root_path, username + ".cookies")
	chapter_file = os.path.join(root_path, "captcha.png")
	try:
		if not os.path.exists(cookies_file):
			print('未找到cookies,执行登陆操作')
			raise
		client.load_cookies(cookies_file)
		if not client.get_account_info():
			print('cookies失效,执行重新登陆')
			raise
	except Exception as e:
		password = input('请输入您的密码:')
		if client.login(username, password, chapter_file):
			client.save_cookies(cookies_file)
			client.get_account_info()
		else:
			sys.exit()
	print('欢迎您:', client.userdata['uname'])
	client.get_notify_count()
	# client.do_reply(5601151, "期待下一集~")

if __name__ == '__main__':
	main()