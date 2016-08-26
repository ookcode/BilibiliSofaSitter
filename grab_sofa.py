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
import grab_sofa_control

def main():
	control = grab_sofa_control.Control()
	control.run()

if __name__ == '__main__':
	main()