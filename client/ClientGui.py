#!/usr/env/bin python
# coding:utf-8
import Tkinter
import tkMessageBox
import time
import ClientConnect
# 登陆主界面
class Login_application(Tkinter.Frame):
	def __init__(self, master=None,clientp = None):
		Tkinter.Frame.__init__(self, master)
		self.grid(row = 0,column = 0,padx = 50,pady = 50)
		self.master.title('聊天客户端')
		self.master.geometry('300x200+700+300')
		self.client = clientp   # 客户端主类指针
		self.createWidgets()

	def createWidgets(self):
		self.idLabel = Tkinter.Label(self, text='账户名:')
		self.idLabel.grid(row = 0)
		self.id_input = Tkinter.Entry(self)
		self.id_input.grid(row = 0, column = 1)
		#############################
		self.passwdLabel = Tkinter.Label(self,text = '密码:')
		self.passwdLabel.grid(row = 1)
		self.passwd_input = Tkinter.Entry(self,show='*')
		self.passwd_input.bind('<Key-Return>',self.quick_login)
		self.passwd_input.grid(row = 1,column = 1)
		########################################
		self.loginButton = Tkinter.Button(self, text='登录',command = self.login)
		self.loginButton.grid(row=2, column=0,ipadx = 20,ipady = 5)
		#######################################
		self.registerButton = Tkinter.Button(self, text='注册', command=self.new_user)
		self.registerButton.grid(row = 2,column = 1,sticky = Tkinter.E,ipadx = 50,ipady = 5)

	def new_user(self):          # 注册用户事件
		self.grid_remove()
		Register_application(clientp=self.client)

	def login(self):     # 登录事件
		if self.id_input.get() == '':
			tkMessageBox.showinfo('提示','请输入账号')
			return
		try:
			self.client.conn_sock.connection() # 连接服务器
			self.client.conn_sock.send_mess('02',self.id_input.get() + '|' + self.passwd_input.get())   # 发送登陆信息
		except IOError:
			tkMessageBox.showerror('错误','无法连接服务器')
			self.quit()
			return
		while self.client.stop_flag == None:
			time.sleep(0.1)
			print 'waiting...'
		if self.client.stop_flag == '01':
			self.grid_remove()
			Main_Room_application(clientp = self.client,username = self.id_input.get())
			print self.id_input.get() + '用户上线'
		elif self.client.stop_flag == '04':
			tkMessageBox.showerror('错误', '用户不存在')
		elif self.client.stop_flag == '02':
			tkMessageBox.showerror('错误', '密码错误')
		elif self.client.stop_flag == '03':
			tkMessageBox.showinfo('提示', '用户已在线')
		self.client.stop_flag = None

	def quick_login(self,event):
		self.login()

# 注册界面
class Register_application(Tkinter.Frame):       #注册界面
	def __init__(self, master=None, clientp = None):
		Tkinter.Frame.__init__(self, master)
		self.grid(row = 0,column = 0,padx = 40,pady = 40)
		self.client = clientp           # 获得客户端主类指针
		self.master.title('注册界面')
		self.createWidgets()

	def createWidgets(self):
		self.idLabel = Tkinter.Label(self, text='账户名:')
		self.idLabel.grid(row = 0)
		self.id_input = Tkinter.Entry(self)
		self.id_input.grid(row = 0, column = 1)
		#############################
		self.passwdLabel = Tkinter.Label(self,text = '密码:')
		self.passwdLabel.grid(row = 1)
		self.passwd_input = Tkinter.Entry(self,show='*')
		self.passwd_input.grid(row = 1,column = 1)
		########################################
		self.passwdLabel1 = Tkinter.Label(self, text='确认密码:')
		self.passwdLabel1.grid(row=2)
		self.passwd_input1 = Tkinter.Entry(self,show = '*')
		self.passwd_input1.grid(row=2, column=1)
		self.passwd_input1.bind('<Key-Return>',self.quick_summit)
		#################################################
		self.okButton = Tkinter.Button(self, text='确认',command = self.summit)
		self.okButton.grid(row=3, column=0,ipadx = 20)
		#######################################
		######################################
		self.backButton = Tkinter.Button(self, text='返回', command=self.back_login)
		self.backButton.grid(row=3, column=1,sticky = Tkinter.E,ipadx = 50)
	
	def pwValue(self,pw): #密码都至少为6位且必须为字母数字以及下划线
		if len(pw) >= 6:
			for i in pw:
				if not (i.isalnum() or i == '_'):
					return False
			return True
		return False
	
	def nameValue(self,name): #用户名和房间号必须为字母数字以及下划线,且不能为'system（此为系统账号）'
		if name == 'system':
			return False
		for i in name:
			if not (i.isalnum() or i == '_') or i.isspace():
				return False
		return True
	def summit(self):
		if self.id_input.get() == '':
			tkMessageBox.showerror('错误','用户名不能为空!')
			return
		if self.passwd_input1.get() != self.passwd_input.get():
			tkMessageBox.showerror('错误', '两次输入的密码不一致!')
			return
		if self.passwd_input.get() == '':
			tkMessageBox.showerror('错误', '密码不能为空!')
			return
		if not self.nameValue(self.id_input.get()):
			tkMessageBox.showerror('错误', '用户名必须为字母数字以及下划线,且不能为system')
			return
		if not self.pwValue(self.passwd_input.get()):
			tkMessageBox.showerror('错误', '密码必须大于6位且为字母数字以及下划线')
			return
		try:
			self.client.conn_sock.connection()
			self.client.conn_sock.send_mess('01',self.id_input.get() + '|'+ self.passwd_input.get())
		except IOError:
			tkMessageBox.showerror('错误','无法连接服务器')
			self.quit()
			return
		while self.client.stop_flag == None:
			time.sleep(0.1)
			print 'waiting...'
		if self.client.stop_flag == '12':
			tkMessageBox.showinfo('消息', '注册失败: ' + '用户名已存在')
		elif self.client.stop_flag == '11':
			tkMessageBox.showinfo('消息', '注册成功\n' + '用户名:' + self.id_input.get())
		self.client.stop_flag = None

	def quick_summit(self,event):
		self.summit()

	def reset_input(self):
		self.id_input.delete(0, Tkinter.END)
		self.passwd_input.delete(0, Tkinter.END)
		self.passwd_input1.delete(0, Tkinter.END)
		return
	def back_login(self):
		self.grid_remove()
		Login_application(clientp=self.client)

# 大厅主界面
class Main_Room_application(Tkinter.Frame):

	def __init__(self, master=None,clientp=None,username = None):
		Tkinter.Frame.__init__(self, master)
		self.grid(row = 0,column = 0,padx = 60,pady = 60)
		self.master.protocol("WM_DELETE_WINDOW", self.back_login)  #基于Python+tkiner的程序，在单机右上角X按钮关闭程序时，
																	#会触发'WM_DELETE_WINDOW'消息，如果可以截获这个消息并改变其行为，就可以禁止关闭程序。
		self.client = clientp
		print '开始绘制主界面.....'
		self.client.main_app = self   # 此时已经打开主界面，在主类中记录
		self.username = username  # 当前用户名
		self.new_person = ''
		self.createWidgets()
		print '绘制完成.....'

	def createWidgets(self):
		self.master.geometry('1200x800+400+100')
		########################################################
		self.roolabel = Tkinter.Label(self,text = '选择房间:')
		self.roolabel.grid(row = 0,column = 0)
		roomlist = ['交友', '科技', '闲扯']
		self.scrollbar = Tkinter.Scrollbar(self)
		self.scrollbar.grid(row = 1,column = 2,ipady = 25)
		self.allroom = Tkinter.Listbox(self,yscrollcommand = self.scrollbar.set,height = 5)
		self.scrollbar['command'] = self.allroom.yview

		self.allroom.grid(row = 1,column = 1,ipady = 10)
		######################################
		self.start_button = Tkinter.Button(self,text = '进入房间',command = self.entry_room)
		self.start_button.grid(row = 2,column = 1,ipady = 10)
		#############################################
		self.create_button = Tkinter.Button(self, text='创建房间',command = self.create_room)
		self.create_button.grid(row=3, column=1,ipady = 10,sticky = Tkinter.N)
		################################################
		self.back_button = Tkinter.Button(self, text='退出登录',command = self.back_login)
		self.back_button.grid(row=4, column=1, ipady=10,sticky = Tkinter.N)
		##############################################
		self.datinglabel = Tkinter.Label(self,text = '聊天大厅')
		self.datinglabel.grid(row = 0,column = 3)
		self.label1 = Tkinter.Label(self, text='当前用户:')
		self.label1.grid(row=0, column=4,sticky = Tkinter.E)

		self.label_name = Tkinter.Label(self,text = self.username)
		self.label_name.grid(row = 0, column = 5,sticky = Tkinter.W)
		##################################################
		self.messscrollbar = Tkinter.Scrollbar(self)
		self.messscrollbar.grid(row = 2,column =4,sticky = Tkinter.W,ipady = 170)

		self.datingtext = Tkinter.Text(self)
		self.datingtext.grid(row = 1, column = 3,rowspan = 4)
		self.messscrollbar.config(command=self.datingtext.yview)
		self.datingtext.config(yscrollcommand = self.messscrollbar.set)
		self.datingtext.edit_modified(True)
		#########################################################
		self.inputlabel = Tkinter.Label(self,text = '输入框:')
		self.inputlabel.grid(row = 5,column = 1,sticky = Tkinter.EW)
		################################################
		self.input_str = Tkinter.Entry(self)
		self.input_str.bind('<Key-Return>',self.quick_send_mess)
		self.input_str.grid(row=5, column=3, ipadx = 250, ipady = 10)
		####################################################
		self.send_button = Tkinter.Button(self,text = '发送',command = self.send_mess)
		self.send_button.grid(row = 5,column = 4,ipadx = 20)
		####################################################
		self.all_player = Tkinter.Listbox(self)
		self.all_player.bind('<Double-Button-1>',self.create_person_chat)         # 双击事件


		self.all_player.grid(row=2, column=5, sticky=Tkinter.N, ipady=100)
		####################################
		self.onlinelabel = Tkinter.Label(self, text='在线用户:')
		self.onlinelabel.grid(row=1, column=5)

		return

	def entry_room(self):
		if str(self.allroom.curselection()) == '()':
			tkMessageBox.showinfo('提示','未选择房间')
			return
		tmp_room = str(self.allroom.get(self.allroom.curselection()[0]))
		if self.client.room_app.has_key(tmp_room):
			return
		for k in self.client.room_app.keys():
			self.client.room_app[k].back_room()
		self.client.conn_sock.send_mess('04', str(self.allroom.get(self.allroom.curselection()[0])) )  # 发送进入房间消息
		top = Tkinter.Toplevel(self)
		new_room = Main_Chat_application(master = top,clientp = self.client,room_name = tmp_room)
		self.client.room_app[tmp_room] = new_room   # 新增一个房间引用
		print '当前进入房间数目:' + str(len(self.client.room_app))
		print '用户进入房间:'+  str(self.allroom.get(self.allroom.curselection()[0]))

	def create_room(self):
		top = Tkinter.Toplevel(self)
		New_room_application(master=top,clientp=self.client)
		return
	def send_mess(self):
		if self.input_str.get() == '':
			return
		self.client.conn_sock.send_mess('11',self.input_str.get())
		print self.input_str.get()
		print self.input_str.get()
		self.input_str.delete(0,Tkinter.END)
		return

	def quick_send_mess(self,event):
		self.send_mess()
	def create_person_chat(self,event):
		tmp_name = str(self.all_player.get(self.all_player.curselection()[0])).strip()
		if self.client.person_app.has_key(tmp_name):
			return
		if tmp_name == self.username:
			return
		top = Tkinter.Toplevel(self)
		new_person = Main_Person_application(master = top, clientp=self.client,
											 person_name = tmp_name)
		self.client.person_app[tmp_name] = new_person  # 新增一个私聊对象引用
		print '当前私聊窗口数目:' + str(len(self.client.person_app))
		print '用户进入私聊窗口:' + str(self.all_player.get(self.all_player.curselection()[0]))

	def create_new_person(self):  # 消息来时弹出窗口
		per_name = self.new_person
		print per_name+'123\n'
		if self.client.person_app.has_key(per_name):
			return
		top = Tkinter.Toplevel(self)
		new_person = Main_Person_application(master=top, clientp=self.client,
											 person_name=per_name)
		self.client.person_app[per_name] = new_person  # 新增一个私聊对象引用
		print '当前私聊窗口数目:' + str(len(self.client.person_app))
		print '弹出私聊窗口:' + per_name
	def back_login(self):
		print self.username + '用户退出登录'
		self.quit()
# 房间主界面
class  Main_Chat_application(Tkinter.Frame):

	def __init__(self, master=None,clientp = None,room_name = None):
		Tkinter.Frame.__init__(self, master)
		self.grid(row = 0,column = 0,padx = 30,pady = 30)
		self.master.title('房间名称:' + room_name)
		self.master.geometry('1000x650+450+150')
		self.master.protocol("WM_DELETE_WINDOW", self.back_room) # 捕获窗口关闭事件
		self.client = clientp
		self.room_name = room_name     # 房间名称
		self.createWidgets()

	def createWidgets(self):
		self.label1 = Tkinter.Label(self,text = '消息窗口:')
		self.label1.grid(row = 0, column = 0,sticky = Tkinter.N)
		self.main_text = Tkinter.Text(self)
		self.main_text.grid(row = 0, column = 1,ipadx = 50,ipady = 50)
		#############################################
		self.label2 = Tkinter.Label(self, text='输入框:')
		self.label2.grid(row=1, column=0, sticky=Tkinter.N)
		self.input_text = Tkinter.Entry(self)
		self.input_text.bind('<Key-Return>',self.quick_send_mess)
		self.input_text.bind('<Shift-Return>', self.quick_send_ans)
		self.input_text.grid(row = 1, column = 1,ipadx = 300,ipady = 10,sticky =Tkinter.W)
		################################
		###################################
		self.sendButton = Tkinter.Button(self,text= '发送/ENTER',command = self.send_mess)
		self.sendButton.grid(row  = 1 ,column = 2,sticky = Tkinter.W,ipadx = 10 ,ipady = 10)

		self.send_ans_Button = Tkinter.Button(self, text='发送game答案/Shift_ENTER', command=self.send_ans)
		self.send_ans_Button.grid(row=2, column=2, sticky=Tkinter.W, ipadx=10, ipady=10)

		self.backButton = Tkinter.Button(self,text = '退出房间',command = self.back_room)
		self.backButton.grid(row = 2, column = 1,sticky = Tkinter.W)
		return
	def back_room(self):
		print '用户退出房间:' + self.room_name
		self.client.conn_sock.send_mess('05',self.room_name)  # 发送退出房间消息
		if self.client.room_app.has_key(self.room_name):
			self.client.room_app.pop(self.room_name)
		print '当前进入房间数目:' + str(len(self.client.room_app))
		self.master.destroy()

	def create_person_chat(self,event):
		tmp_name = str(self.all_player.get(self.all_player.curselection()[0])).strip()
		if self.client.person_app.has_key(tmp_name):
			return
		top = Tkinter.Toplevel(self)
		new_person = Main_Person_application(master=top, clientp=self.client,
											 person_name = tmp_name)
		self.client.person_app[tmp_name] = new_person  # 新增一个私聊对象引用
		print '当前私聊窗口数目:' + str(len(self.client.person_app))
		print '用户进入私聊窗口:' + str(self.all_player.get(self.all_player.curselection()[0]))

	def send_mess(self):
		if self.input_text.get() == '':
			return
		self.client.conn_sock.send_mess('12', self.input_text.get())
		print self.input_text.get()
		self.input_text.delete(0,Tkinter.END)
		return
		
		
	def send_ans(self):
		if self.input_text.get() == '':
			return
		self.client.conn_sock.send_mess('70',self.input_text.get()) # 发送游戏答案
		self.main_text.insert(Tkinter.END, self.client.main_app.username + ': 游戏回答: ' + self.input_text.get() + '\n')  # 只有自己可见
		self.input_text.delete(0,Tkinter.END)
		return
		

	def quick_send_mess(self,event):
		self.send_mess()

	def quick_send_ans(self,event):
		self.send_ans()
	# 新建房间界面
class New_room_application(Tkinter.Frame):

	def __init__(self, master=None,clientp=None):
		Tkinter.Frame.__init__(self, master)
		self.grid(row = 0,column = 0,padx = 60,pady = 60)
		self.master.protocol("WM_DELETE_WINDOW", self.close_create)
		self.client = clientp
		self.createWidgets()

	def createWidgets(self):
		self.idLabel = Tkinter.Label(self, text='房间名:')
		self.idLabel.grid(row=0)
		self.id_input = Tkinter.Entry(self)
		self.id_input.bind('<Key-Return>',self.quick_new_room)
		self.id_input.grid(row=0, column=1)
		#############################################
		self.createButton = Tkinter.Button(self, text='创建', command=self.new_room)
		self.createButton.grid(row=1, column=1, ipadx=20, ipady=5)

	def new_room(self):
		for i in range(self.client.main_app.allroom.size()):
			if self.id_input.get() == self.client.main_app.allroom.get(i):
				tkMessageBox.showinfo('提示', '已存在该名称')
				return
		for ch in  self.id_input.get():
			if not (ch.isalnum() or ch == '_'):
				tkMessageBox.showinfo('提示', '房间名必须为下划线或者是字母数字')
				return
		print '创建新房间:' + self.id_input.get()
		self.client.conn_sock.send_mess('03',self.id_input.get())
		tkMessageBox.showinfo('提示','创建成功')
		self.master.destroy()

	def close_create(self):
		self.master.destroy()

	def quick_new_room(self,event):
		self.new_room()

# 私聊界面
class Main_Person_application(Tkinter.Frame):

	def __init__(self, master=None,clientp = None,person_name = None):
		Tkinter.Frame.__init__(self, master)
		self.grid(row = 0,column = 0,padx = 30,pady = 30)
		self.master.title('对方名称:' + person_name)
		self.master.geometry('880x550+500+150')
		self.master.protocol("WM_DELETE_WINDOW", self.back_chat) # 捕获窗口关闭事件
		self.client = clientp
		self.person_name = person_name     # 对方名称
		self.createWidgets()

	def createWidgets(self):
		self.label1 = Tkinter.Label(self,text = '消息窗口:')
		self.label1.grid(row = 0, column = 0,sticky = Tkinter.N)
		self.main_text = Tkinter.Text(self)
		self.main_text.grid(row = 0, column = 1,ipadx = 20,ipady = 5)
		#############################################
		self.label2 = Tkinter.Label(self, text='输入框:')
		self.label2.grid(row=1, column=0, sticky=Tkinter.N)
		self.input_text = Tkinter.Entry(self)
		self.input_text.bind('<Key-Return>',self.quick_send_mess)
		self.input_text.grid(row = 1, column = 1,ipadx = 200,ipady = 10,sticky =Tkinter.W)
		################################
		self.sendButton = Tkinter.Button(self,text= '发送',command = self.send_mess)
		self.sendButton.grid(row  = 1 ,column = 2,sticky = Tkinter.W,ipadx = 10 ,ipady = 10)
		self.backButton = Tkinter.Button(self,text = '退出窗口',command = self.back_chat)
		self.backButton.grid(row = 2, column = 1,sticky = Tkinter.W)
		return

	def back_chat(self):
		print '用户退出私人窗口:' + self.person_name
		if self.client.person_app.has_key(self.person_name):
			self.client.person_app.pop(self.person_name)
		print '当前私聊窗口数目:' + str(len(self.client.person_app))
		self.master.destroy()

	def send_mess(self):
		if self.input_text.get() == '':
			return
		self.client.conn_sock.send_mess('13',self.person_name + '|' + self.input_text.get())
		print self.input_text.get()
		self.main_text.insert(Tkinter.END,self.client.main_app.username + ': ' + self.input_text.get()+ '\n')
		self.input_text.delete(0,Tkinter.END)

	def quick_send_mess(self,event):
		self.send_mess()

