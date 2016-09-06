#!/usr/bin/python3
#coding:utf-8

from functools import partial
from datetime import datetime
import time
import math
import threading
import grab_sofa_model
import grab_sofa_view

###################################
#
#	MVC - Control
#
####################################
class Control():
	def __init__(self):
		self.view = grab_sofa_view.View()
		self.model = grab_sofa_model.Model()
		for av_id in self.model.data_dic.keys():
			self.view.add_row(self.model.data_dic[av_id])
		self._bind_events()
		t = threading.Thread(target=self._update)
		t.start()

	def _bind_events(self):
		self.view.create_btn.configure(command = self._create)
		for av_id in self.model.data_dic.keys():
			row = self.view.rows[av_id]
			row["operate_btn"].configure(command = partial(self._operate, av_id))
			row["delete_btn"].configure(command = partial(self._delete, av_id))

	def _create(self):
		try:
			av_id = int(self.view.create_id.get())
		except Exception as e:
			print("error can't create because:")
			print(e)
			return
		data = self.model.request_data(av_id)
		data['stoped'] = True
		self.model.add_data(av_id, data)
		self.view.add_row(data)
		self._bind_events()
		self.model.write_cache()

	def _delete(self, av_id):
		del self.model.data_dic[av_id]
		self.view.clear()
		for av_id in self.model.data_dic.keys():
			self.view.add_row(self.model.data_dic[av_id])
		self._bind_events()
		self.model.write_cache()

	def _operate(self, av_id):
		data = self.model.data_dic[av_id]
		if data['stoped']:
			data = self.model.request_data(av_id)
			data['stoped'] = False
			self.model.add_data(av_id, data)
			self.view.update_row(av_id, data)
			self.model.write_cache()
		else:
			data['stoped'] = True
			self.view.update_operate_btn(av_id, data['stoped'])

	def _update(self):
		while True:
			now = datetime.now()
			for av_id in self.model.data_dic.keys():
				data = self.model.data_dic[av_id]
				# 不操作停止状态的数据
				if data['stoped']:
					continue
				##################
				# 午时已到
				##################
				if now > data['nextdate']:
					dt = now - data['nextdate']
					# 当前日期超过预计更新日期太久，判定为今日停更，进入下一周期
					if dt.seconds >= self.model.max_over_minute * 60:
						print("{}超过预计更新时间超过{}分钟，今日停更，进入下一个周期！".format(av_id, self.model.max_over_minute))
						self.model.defer_to_next_period(av_id)

					# 开始请求服务器数据
					else:
						self.view.update_countdown_lbl(av_id, "刷新中{}".format(dt.seconds))
						new_data = self.model.request_data(av_id)
						print("{} {}".format(av_id, dt.seconds))
						print(new_data['lastdate'], data['nextdate'])
						# 当发现有更新时
						if new_data['lastdate'] == data['nextdate']:
							print(data['title'], "发现更新")
							print(new_data)
							# 抢沙发
							reply = "稳坐二楼的千万手速王(｀_´)ゞ"
							self.model.request_reply(new_data['last_id'], reply)
						self.model.add_data(av_id, new_data)

				######################
				# 午时未到，更新倒计时
				######################
				else:
					dt = data['nextdate'] - now
					seconds = dt.seconds
					minutes = math.floor(seconds / 60)
					hours = math.floor(minutes / 60) + dt.days * 24
					second = seconds % 60
					minute = minutes % 60
					self.view.update_countdown_lbl(av_id, "%d:%02d:%02d" % (hours, minute, second))
			time.sleep(1)

	def run(self):
		self.view.run()