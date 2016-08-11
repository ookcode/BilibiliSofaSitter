#!/usr/bin/python3
#coding=utf-8
############################################################
#
#	监听番剧更新并抢沙发（需加入定时任务）
#	第一个参数为番剧ID，示例：python3 handle_update.py 5070
#	第二个参数为最大监听分钟数(小于24*60)，超过该时间自动停止脚本，不填则默认24*60分钟
#	crontab -e编辑定时任务列表
#	每天7点59分(监听番剧5070)示例:
#	59 7 * * * /usr/local/bin/python3 yourpath/handle_update.py 5070 >> yourpath/handle_update.log
#	Tips:使用crontab执行python可能会报'ascii' codec can't encode character错误
#	解决方案：在crontab -e的顶部加上LC_CTYPE="en_US.UTF-8"
#
############################################################
import os,sys
if not sys.version_info[0] == 3:
	print("当前脚本只能在python3.x下运行，请更换您的python版本！")
	sys.exit()

import api
import json
import time

def main():
	client = api.Client()
	client.cookies_login()
	try:
		handle_id = int(sys.argv[1])		#监听番剧ID
	except Exception as e:
		print('error:番剧ID错误，请检查第一个参数是否正确')
		sys.exit()

	max_handle_minutes = 24 * 60	#最大监听分钟数
	try:
		handle_minutes = int(sys.argv[2])	#监听分钟数
	except Exception as e:
		handle_minutes = 0
	if handle_minutes <= 0 or handle_minutes > max_handle_minutes:
		handle_minutes = max_handle_minutes
	print(handle_minutes)
	start_episodes = None		#初始数据
	start_count = 0				#初始番剧集数
	reply = "我是千万手速王 - ( ゜- ゜)つロ"

	for index in range(0, handle_minutes * 60):
		data = client.get_bangumi_detail(handle_id)
		episodes = data['episodes']
		count = len(episodes)
		if index == 0:
			start_episodes = episodes
			start_count = count
			print("开始监听番剧：",data['title'], "至多监听{}分钟".format(handle_minutes))
		print(index, "上次更新 {}".format(episodes[0]['update_time']))
		if start_count < count:
			av_id = int(episodes[0]['av_id'])
			print("发现更新{}，监听结束".format(av_id))
			client.do_reply(av_id, reply)
			break
		time.sleep(1)

if __name__ == '__main__':
	main()