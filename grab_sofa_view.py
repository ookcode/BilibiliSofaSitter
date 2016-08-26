#!/usr/bin/python3
#coding:utf-8
import tkinter as tk
from tkinter import ttk

###################################
#
#	MVC - View
#
####################################
class View():
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili')
		self.root.geometry('600x400')
		self.root.resizable(width=False, height=False)
		self.col_count = 6
		self.rows = {}
		for i in range(0, self.col_count):
			self.root.columnconfigure(i, weight=1)
		panel = ttk.Labelframe(self.root, text="欢迎光临")
		panel.columnconfigure(0, weight=1)
		panel.grid(row=0, column=0, columnspan=self.col_count, stick='we')

		self.create_id = tk.StringVar()
		self.create_id.set("请输入番剧ID")

		self.create_entry = tk.Entry(panel, textvariable=self.create_id)
		self.create_btn = tk.Button(panel, text='create')

		self.create_entry.grid(row=0, column=1)
		self.create_btn.grid(row=0, column=2)

		id_lbl = tk.Label(self.root, text="ID")
		title_lbl = tk.Label(self.root, text="名称")
		uptime_lbl = tk.Label(self.root, text="更新时间")
		countdown_lbl = tk.Label(self.root, text="倒计时")
		status_lbl = tk.Label(self.root, text="状态")

		id_lbl.grid(row=1, column=0)
		title_lbl.grid(row=1, column=1)
		uptime_lbl.grid(row=1, column=2)
		countdown_lbl.grid(row=1, column=3)
		status_lbl.grid(row=1, column=4)

	# 增
	def add_row(self, data):
		index = len(self.rows)
		av_id = data['id']
		row_items = {}
		id_lbl = tk.Label(self.root, text="")
		title_lbl = tk.Label(self.root, text="")
		uptime_lbl = tk.Label(self.root, text="")
		countdown_lbl = tk.Label(self.root, text="")
		operate_btn = tk.Button(self.root, text="")
		delete_btn = tk.Button(self.root, text='del')

		row_items["id_lbl"] = id_lbl
		row_items["title_lbl"] = title_lbl
		row_items["uptime_lbl"] = uptime_lbl
		row_items["countdown_lbl"] = countdown_lbl
		row_items["operate_btn"] = operate_btn
		row_items["delete_btn"] = delete_btn

		id_lbl.grid(row=index + 2, column=0)
		title_lbl.grid(row=index + 2, column=1)
		uptime_lbl.grid(row=index + 2, column=2)
		countdown_lbl.grid(row=index + 2, column=3)
		operate_btn.grid(row=index + 2, column=4)
		delete_btn.grid(row=index + 2, column=5)

		self.rows[av_id] = row_items
		self.update_row(av_id, data)

	# 清屏
	def clear(self):
		for row_key in self.rows.keys():
			row = self.rows[row_key]
			for key in row.keys():
				row[key].grid_forget()
		self.rows.clear()
	
	# 改
	def update_row(self, av_id, data):
		row = self.rows[av_id]
		uptime_text = "周{} {}".format((',').join(str(i) for i in data['weekday']), data['uptime'])
		row["id_lbl"].configure(text = str(data['id']))
		row["title_lbl"].configure(text = data['title'])
		row["uptime_lbl"].configure(text = uptime_text)
		self.update_operate_btn(av_id, data['stoped'])

	# 改变操作按钮状态
	def update_operate_btn(self, av_id, stoped):
		row = self.rows[av_id]
		if stoped:
			row["countdown_lbl"].configure(text = "--:--:--")
			row["operate_btn"].configure(text = "stoped")
		else:
			row["operate_btn"].configure(text = "running")

	# 更新倒计时
	def update_countdown_lbl(self, av_id, timestr):
		row = self.rows[av_id]
		row["countdown_lbl"].configure(text = timestr)

	# ui运行
	def run(self):
		self.root.mainloop()