#!/usr/bin/python3
#coding=utf-8
import os,sys
import api
import json
from datetime import datetime
from datetime import timedelta

g_root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
g_cache_path = os.path.join(g_root_path, 'cache.json')

###################################
#
#	MVC - Model
#
####################################
class Model():
	def __init__(self):
		self.max_over_minute = 120
		self.data_dic = self._read_cache()
		self.api = api.Client()
		self.api.cookies_login()

	def _read_cache(self):
		try:
			f = open(g_cache_path, 'r')
			cache_data = json.loads(f.read())
			f.close()
			data_dic = {}
			for item in cache_data:
				data = {}
				data['id'] = item['id']
				data['title'] = item['title']
				data['weekday'] = []
				data['uptime'] = item['uptime']
				for weekday in item['weekday'].split(","):
					data['weekday'].append(int(weekday))
				data['stoped'] = True
				data_dic[data['id']] = data
			return data_dic
		except Exception as e:
			print('error read cache.json:', e)
			return {}

	def _cal_delta_day(self, weeklist, today_weekday):
		# 周更
		if len(weeklist) == 1:
			return 7
		# 非周更
		else:
			for index, weekday in enumerate(weeklist):
				# TODO:处理在非计划时间内突然更新了的情况
				if weekday == today_weekday:
					try:
						next_weekday = weeklist[index + 1]
					except Exception as e:
						next_weekday = weeklist[0]
					break
			if next_weekday > today_weekday:
				return next_weekday - today_weekday
			else:
				return 7 - today_weekday + next_weekday

	def defer_to_next_period(self, av_id):
		data = self.data_dic[av_id]
		delta_day = self._cal_delta_day(data['weekday'], data['lastdate'].isoweekday())
		data['nextdate'] = data['nextdate'] + timedelta(delta_day)

	def write_cache(self):
		cache_list = []
		for key in self.data_dic.keys():
			data = self.data_dic[key]
			cache = {}
			cache['id'] = data['id']
			cache['title'] = data['title']
			cache['weekday'] = (',').join(str(i) for i in data['weekday'])
			cache['uptime'] = data['uptime']
			cache_list.append(cache)

		f = open(g_cache_path, 'w')
		f.write(json.dumps(cache_list))
		f.close()

	def add_data(self, av_id, data):
		if av_id in self.data_dic.keys():
			for key in data.keys():
				self.data_dic[av_id][key] = data[key]
		else:
			self.data_dic[av_id] = data

	def request_data(self, av_id):
		info = self.api.get_bangumi_detail(av_id)
		if not info:
			print("{} not exists".format(av_id))
			return None	
		if info['pub_time'] == "":
			print("{} pub_time unknow".format(av_id))
			return None
		# if int(info['is_finish']) != 0:
		# 	print(info['title'], "is finished")
		# 	return None
		data = {}
		data['id'] = int(info['season_id'])
		data['title'] = info['title']
		data['uptime'] = info['pub_time'].split(" ")[1]
		weekday = int(info['weekday'])
		if weekday == 0:
			data['weekday'] = [7]
		elif weekday == -1:
			data['weekday'] = [1,2,3,4,5]
		else:
			data['weekday'] = [weekday]
		episodes = info['episodes']
		lastdate = episodes[0]['update_time'].split(" ")[0] + " " + data['uptime']
		# lastdate = "2016-08-25 08:42:00" #测试数据
		data['lastdate'] = datetime.strptime(lastdate, "%Y-%m-%d %H:%M:%S")
		data['last_id'] = int(episodes[0]['av_id'])
		# 计算下次更新时间
		delta_day = self._cal_delta_day(data['weekday'], data['lastdate'].isoweekday())
		data['nextdate'] = data['lastdate'] + timedelta(delta_day)
		return data

	def request_reply(self, last_id, content):
		self.api.do_reply(last_id, content)
