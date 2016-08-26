#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	bilibli api
#
############################################################
import os,sys
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
			cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
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
			print("登陆失败", info)
			return False
		except Exception as e:
			#登陆成功
			return True
			
	#使用cookies登陆
	def cookies_login(self):
		root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
		#读取配置文件中的username
		config_path = os.path.join(root_path, 'username.config')
		try:
			f = open(config_path, 'r')
			config = json.load(f)
			username = config['username']
		except Exception as e:
			print("username.config文件不存在或内容错误，请重新执行一次login.py")
			sys.exit()
		finally:
			f.close()
		#读取cookies文件
		cookies_file = os.path.join(root_path, username + ".cookies")
		if not os.path.exists(cookies_file):
			print(username + '.cookies不存在，请重新执行一次login.py')
			sys.exit()
		self.load_cookies(cookies_file)
		if not self.get_account_info():
			print(username + '.cookies失效，请重新执行一次login.py')
			sys.exit()
		print('欢迎您:', self.userdata['uname'])
		return self.userdata['uname']

	#获取个人信息
	def get_account_info(self):
		response = self.session.get('https://account.bilibili.com/home/userInfo')
		data = json.loads(response.content.decode('utf-8'))
		try:
			if data['status'] == True:
				self.userdata = data['data']
				return True
		except Exception as e:
			print(e)
		return False

	#获取个人通知消息个数
	def get_notify_count(self):
		#CaptchaKey
		response = self.session.get('http://www.bilibili.com/plus/widget/ajaxGetCaptchaKey.php?js')
		captcha = response.text.split('\"')[1]
		response = self.session.get('http://message.bilibili.com/api/notify/query.notify.count.do?captcha=' + captcha)

	#抢沙发
	def do_reply(self, avid, content):
		print("开始抢沙发：", content)
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

	#获取番剧详情
	def get_bangumi_detail(self, bangumi_id):
		response = self.session.post("http://bangumi.bilibili.com/jsonp/seasoninfo/{}.ver".format(bangumi_id))
		data = json.loads(response.content.decode('utf-8'))
		try:
			if data['code'] == 0:
				return data['result']
		except Exception as e:
			print('error', e)