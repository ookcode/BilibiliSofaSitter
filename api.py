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

	def load_cookies_str(self, path):
		with open(path, 'rb') as f:
			cookies = f.read()
			self.session.headers['cookie'] = cookies
			self.userdata = {}

	def load_cookies(self, path):
		with open(path, 'rb') as f:
			self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
			self.userdata = {}

	def save_cookies(self, path):
		with open(path, 'wb') as f:
			cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
			pickle.dump(cookies_dic, f)

			
	#使用cookies登陆
	def cookies_login(self):
		root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
		cookies_file = None
		# 当前目录查找后缀.cookies的文件
		for f in os.listdir(root_path):
			if os.path.splitext(f)[1] == ".cookies":
				cookies_file = os.path.join(root_path, f)
				break
		if not os.path.exists(cookies_file):
			print("在当前目录下未找到.cookies文件.")
			sys.exit()
		# 读取cookies文件
		self.load_cookies_str(cookies_file)
		if not self.get_account_info():
			print(username + '.cookies失效，，请重新获取')
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
		response = self.session.get("https://bangumi.bilibili.com/jsonp/seasoninfo/{}.ver".format(bangumi_id))
		content = response.content.decode('utf-8')
		begin = "seasonListCallback("
		end = ");"
		content = content[len(begin): - len(end)]
		print(content)
		data = json.loads(content)
		try:
			if data['code'] == 0:
				return data['result']
		except Exception as e:
			print('error', e)