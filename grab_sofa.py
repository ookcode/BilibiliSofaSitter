#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	监听番剧更新并抢沙发
#
############################################################
import os,sys
if not sys.version_info[0] == 3:
	print("当前脚本只能在python3.x下运行，请更换您的python版本！")
	sys.exit()

import api
import time
from datetime import datetime

##############################################
#
# 返回时、分、秒
# @param time_str	%H:%M:%S 格式时间字符串
# @return hour, minute, second
# 
##############################################
def get_hms(time_str):
	hms = time_str.split(".")[0].split(":")
	hour = int(hms[0])		#时
	minute = int(hms[1])	#分
	second = int(hms[2])	#秒
	return hour, minute, second

##############################################
#
# 返回年、月、日
# @param time_str	%Y-%m-%d 格式时间字符串
# @return year, month, day
# 
##############################################
def get_ymd(time_str):
	ymd = time_str.split("-")
	year = int(ymd[0])		#年
	month = int(ymd[1])		#月
	day = int(ymd[2])		#日
	return year, month, day

def main():
	client = api.Client()
	client.cookies_login()

	try:
		handle_id = int(input("请输入要监听的番剧ID："))
	except Exception as e:
		print(e)
		sys.exit()

	#获取番剧详情
	start_data = client.get_bangumi_detail(handle_id)
	if not start_data:
		print("番剧{}不存在".format(handle_id))
		sys.exit()
	start_episodes = start_data['episodes']

	#是否完结
	is_finish = int(start_data['is_finish'])
	if is_finish != 0:
		print(start_data['title'])
		print("非常遗憾，该番剧已经完结了")
		sys.exit()

	#更新周期
	weekday = int(start_data['weekday'])
	weekday_list = []
	if weekday == -1:
		user_input = input("该番剧更新周期不明，请输入更新周期(如1,3,5更新请输入1,3,5)：")
		user_input = user_input.strip()
		for item in user_input.split(","):
			weekday_list.append(int(item))
	else:
		weekday_list.append(weekday)

	#更新时间
	today_updated = False
	if len(start_episodes) == 0:
		update_time = input("暂无该番剧的更新记录，请输入预计更新时间(%H:%M:%S)：")
		update_time = update_time.strip()
	else:
		pub_time = start_data['pub_time']
		update_time = pub_time.split(" ")[1]
		#判断今日是否更新
		lasted_time = start_episodes[0]['update_time']
		year, month, day = get_ymd(lasted_time.split(' ')[0])
		now = datetime.now()
		if now.year == year and now.month == month and now.day == day:
			today_updated = True

	#提示语
	print("{} 每周{}的{}更新".format(start_data['title'], weekday_list, update_time))
	reply = input("请输入沙发内容：").strip()
	if today_updated:
		print("该番剧今日已更新")
	print("正在等待下一次更新，请不要关闭该程序......")

	#监听
	hour, minute, second = get_hms(update_time)
	refresh_times = 0		#刷新次数
	focus_times = 30 		#集中快速刷新次数
	max_times = 60 * 10		#最大刷新次数（10分钟）
	while True:
		now = datetime.now()
		if now.weekday() in weekday_list:
			if not today_updated and now.hour >= hour and now.minute >= minute and now.second >= second:
				#开始刷新
				if refresh_times >= max_times:
					print('刷新次数已达上限!')
					break
				data = client.get_bangumi_detail(handle_id)
				episodes = data['episodes']
				if len(episodes) > 0:
					lasted_time = episodes[0]['update_time']
					year, month, day = get_ymd(lasted_time.split(' ')[0])
					if now.year == year and now.month == month and now.day == day:
						av_id = int(episodes[0]['av_id'])
						print(now, '发现更新{}'.format(av_id))
						client.do_reply(av_id, reply)
						break
					else:
						print(now, '尚未更新')
				else:
					print(now, '尚未更新')				
				#集中快速刷新
				if refresh_times < focus_times:
					time.sleep(0.4)
				else:
					time.sleep(0.9)
				refresh_times = refresh_times + 1
		time.sleep(0.1)
if __name__ == '__main__':
	main()