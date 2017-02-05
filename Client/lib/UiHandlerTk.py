# coding:utf-8
from Tkinter import *
import re
import network
import netstream
import game_controller


class UiHandler(object):
    def __init__(self):
        super(UiHandler, self).__init__()
        self.login_ui = None
        self.register_ui = None
        self.reset_ui = None
        self.username_entry = None
        self.pwd_entry = None
        self.pwd_confirm_entry = None
        self.safety_code_entry = None
        self.wrong_tip = None
        self.Flag = False

    def show_login_ui(self):
        self.clear_all_entry()
        self.login_ui = Tk()
        self.login_ui.title('登录界面')
        frame = Frame(self.login_ui)
        frame.pack(padx=8, pady=15, ipadx=3)

        lab1 = Label(frame, text='用户名：')
        lab1.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        u = StringVar()
        user = Entry(frame, textvariable=u)
        user.grid(row=0, column=1, sticky=EW, columnspan=2)
        self.username_entry = user

        lab2 = Label(frame, text='密码：')
        lab2.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        p = StringVar()
        password = Entry(frame, show='*', textvariable=p)
        password.grid(row=1, column=1, sticky=EW, columnspan=2)
        self.pwd_entry = password

        lab3 = Label(frame, fg='red', text='')
        lab3.grid(row=2, columnspan=3, padx=5, pady=5, sticky=EW)
        self.wrong_tip = lab3

        btn1 = Button(frame, text='登录', command=self.execute_login, default='active')
        btn1.grid(row=3, sticky=EW, columnspan=3)

        btn2 = Button(frame, text='注册账户', command=self.show_register_ui)
        btn2.grid(row=4, sticky=EW, columnspan=3)

        btn3 = Button(frame, text='忘记密码？', command=self.show_reset_ui)
        btn3.grid(row=5, sticky=EW, columnspan=3)

        x = (self.login_ui.winfo_screenwidth() - self.login_ui.winfo_reqwidth()) / 2
        y = (self.login_ui.winfo_screenheight() - self.login_ui.winfo_reqheight()) / 2
        self.login_ui.geometry("+%d+%d" % (x, y))
        self.login_ui.resizable(False, False)
        if self.register_ui is not None:
            self.register_ui.destroy()
            self.register_ui = None
        if self.reset_ui is not None:
            self.reset_ui.destroy()
            self.reset_ui = None
        self.login_ui.mainloop()

    def show_register_ui(self):
        self.clear_all_entry()
        self.register_ui = Tk()
        self.register_ui.title('注册界面')
        frame = Frame(self.register_ui)
        frame.pack(padx=8, pady=15, ipadx=3)

        lab1 = Label(frame, text='用户名：')
        lab1.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        u = StringVar()
        user = Entry(frame, textvariable=u)
        user.grid(row=0, column=1, sticky=EW, columnspan=2)
        self.username_entry = user

        lab2 = Label(frame, text='密码：')
        lab2.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        p = StringVar()
        password = Entry(frame, show='*', textvariable=p)
        password.grid(row=1, column=1, sticky=EW, columnspan=2)
        self.pwd_entry = password

        lab3 = Label(frame, text='重复密码：')
        lab3.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        Rp = StringVar()
        Rpassword = Entry(frame, show='*', textvariable=Rp)
        Rpassword.grid(row=2, column=1, sticky=EW, columnspan=2)
        self.pwd_confirm_entry = Rpassword

        lab4 = Label(frame, text='安全码：')
        lab4.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        s = StringVar()
        safe = Entry(frame, textvariable=s)
        safe.grid(row=3, column=1, sticky=EW, columnspan=2)
        self.safety_code_entry = safe

        lab5 = Label(frame, fg='red', text='')
        lab5.grid(row=4, columnspan=2, padx=5, pady=5, sticky=E)
        self.wrong_tip = lab5

        btn1 = Button(frame, text='提交注册', command=self.execute_register)
        btn1.grid(row=5, sticky=EW, columnspan=3)

        btn2 = Button(frame, text='返回登录', command=self.show_login_ui)
        btn2.grid(row=6, sticky=EW, columnspan=3)

        x = (self.register_ui.winfo_screenwidth() - self.register_ui.winfo_reqwidth()) / 2
        y = (self.register_ui.winfo_screenheight() - self.register_ui.winfo_reqheight()) / 2
        self.register_ui.geometry("+%d+%d" % (x, y))
        self.register_ui.resizable(False, False)
        if self.login_ui is not None:
            self.login_ui.destroy()
            self.login_ui = None
        if self.reset_ui is not None:
            self.reset_ui.destroy()
            self.reset_ui = None
        self.register_ui.mainloop()

    def show_reset_ui(self):
        self.clear_all_entry()
        self.reset_ui = Tk()
        self.reset_ui.title('密码重置界面')
        frame = Frame(self.reset_ui)
        frame.pack(padx=8, pady=15, ipadx=3)

        lab1 = Label(frame, text='用户名：')
        lab1.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        u = StringVar()
        user = Entry(frame, textvariable=u)
        user.grid(row=0, column=1, sticky=EW, columnspan=2)
        self.username_entry = user

        lab2 = Label(frame, text='安全码：')
        lab2.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        s = StringVar()
        safe = Entry(frame, textvariable=s)
        safe.grid(row=1, column=1, sticky=EW, columnspan=2)
        self.safety_code_entry = safe

        lab3 = Label(frame, text='密码：')
        lab3.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        p = StringVar()
        password = Entry(frame, show='*', textvariable=p)
        password.grid(row=2, column=1, sticky=EW, columnspan=2)
        self.pwd_entry = password

        lab4 = Label(frame, text='重复密码：')
        lab4.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        Rp = StringVar()
        Rpassword = Entry(frame, show='*', textvariable=Rp)
        Rpassword.grid(row=3, column=1, sticky=EW, columnspan=2)
        self.pwd_confirm_entry = Rpassword

        lab5 = Label(frame, fg='red', text='')
        lab5.grid(row=4, columnspan=2, padx=5, pady=5, sticky=E)
        self.wrong_tip = lab5

        btn1 = Button(frame, text='提交重置', command=self.execute_reset)
        btn1.grid(row=5, sticky=EW, columnspan=3)

        btn2 = Button(frame, text='返回登录', command=self.show_login_ui)
        btn2.grid(row=6, sticky=EW, columnspan=3)

        x = (self.reset_ui.winfo_screenwidth() - self.reset_ui.winfo_reqwidth()) / 2
        y = (self.reset_ui.winfo_screenheight() - self.reset_ui.winfo_reqheight()) / 2
        self.reset_ui.geometry("+%d+%d" % (x, y))
        self.reset_ui.resizable(False, False)
        if self.login_ui is not None:
            self.login_ui.destroy()
            self.login_ui = None
        if self.register_ui is not None:
            self.register_ui.destroy()
            self.register_ui = None
        self.reset_ui.mainloop()

    def execute_login(self):
        login_name_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,12}$')
        pwd_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$')
        if not login_name_re.match(self.username_entry.get()):
            self.wrong_tip['text'] = '用户名为6~12位数字和字母组合'
        elif not pwd_re.match(self.pwd_entry.get()):
            self.wrong_tip['text'] = '密码为6~16位数字和字母组合'
        else:
            if not network.connected:
                self.wrong_tip['text'] = "服务器连接已断开"
            else:
                network.request_login(self.username_entry.get(), self.pwd_entry.get())
                while not self.Flag:
                    self.receiveServer()
                self.Flag = False

    def execute_register(self):
        login_name_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,12}$')
        pwd_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$')
        safety_code_re = re.compile(r'^[0-9]{6,12}$')
        if not login_name_re.match(self.username_entry.get()):
            self.wrong_tip['text'] = '用户名为6~12位数字和字母组合'
        elif not pwd_re.match(self.pwd_entry.get()):
            self.wrong_tip['text'] = '密码为6~16位数字和字母组合'
        elif not self.pwd_entry.get() == self.pwd_confirm_entry.get():
            self.wrong_tip['text'] = '两次密码输入不一致'
        elif not safety_code_re.match(self.safety_code_entry.get()):
            self.wrong_tip['text'] = '安全码为6~12位的纯数字'
        else:
            if not network.connected:
                self.wrong_tip['text'] = "服务器连接已断开"
            else:
                network.request_register(self.username_entry.get(), self.pwd_entry.get(),
                                         self.pwd_confirm_entry.get(), self.safety_code_entry.get())
                while not self.Flag:
                    self.receiveServer()
                self.Flag = False

    def execute_reset(self):
        login_name_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,12}$')
        pwd_re = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$')
        safety_code_re = re.compile(r'^[0-9]{6,12}$')
        if not login_name_re.match(self.username_entry.get()):
            self.wrong_tip['text'] = '用户名为6~12位数字和字母组合'
        elif not pwd_re.match(self.pwd_entry.get()):
            self.wrong_tip['text'] = '密码为6~16位数字和字母组合'
        elif not self.pwd_entry.get() == self.pwd_confirm_entry.get():
            self.wrong_tip['text'] = '两次密码输入不一致'
        elif not safety_code_re.match(self.safety_code_entry.get()):
            self.wrong_tip['text'] = '安全码为6~12位的纯数字'
        else:
            if not network.connected:
                self.wrong_tip['text'] = "服务器连接已断开"
            else:
                network.request_reset_password(self.username_entry.get(), self.pwd_entry.get(),
                                               self.pwd_confirm_entry.get(), self.safety_code_entry.get())
                while not self.Flag:
                    self.receiveServer()
                self.Flag = False

    def clear_all_entry(self):
        self.username_entry = None
        self.pwd_entry = None
        self.pwd_confirm_entry = None
        self.safety_code_entry = None
        self.wrong_tip = None

    def receiveServer(self):
        if not network.connected:
            self.wrong_tip['text'] = "服务器连接已断开"
            return
        data = netstream.read(network.sock)
        if data == netstream.TIMEOUT or data == netstream.EMPTY:
            self.wrong_tip['text'] = "正在请求，请等待..."
            return
        elif data == netstream.CLOSED:
            self.wrong_tip['text'] = "服务器已关闭"
            return

        # 请求注册的返回信息， 1：注册成功  0：用户名已存在  -1：服务器异常
        if 'register' in data:
            if data['register'] == -1:
                self.wrong_tip['text'] = "服务器异常"
            elif data['register'] == 0:
                self.wrong_tip['text'] = "用户名已存在"
            else:
                self.wrong_tip['text'] = "注册成功"
            self.Flag = True
            return

        # 请求登录的返回信息，  1：登录成功  0：账号/密码错误  -1：服务器异常
        if 'login' in data:
            if data['login'] == -1:
                self.wrong_tip['text'] = "服务器异常"
            elif data['login'] == 0:
                self.wrong_tip['text'] = "账号/密码有误"
            elif data['login'] == 1:
                game_controller.login_name = self.username_entry.get()
                print game_controller.login_name
                print "登录成功"
                self.login_ui.destroy()

                start_botton = game_controller.SingleGameStartMenu()
                game_controller.gameLayer.add(start_botton, z=20, name="start_button")
                game_controller.gameLayer.remove("login_button")
                game_controller.gameLayer.get("login_label").element.text = u"欢迎，" + game_controller.login_name
            self.Flag = True
            return

        # 请求重置密码的返回信息， 1：重置成功  0：账号/安全码错误  -1：服务器异常
        if 'reset_password' in data:
            if data['reset_password'] == -1:
                self.wrong_tip['text'] = "服务器异常"
            elif data['reset_password'] == 0:
                self.wrong_tip['text'] = "账号/安全码错误"
            else:
                self.wrong_tip['text'] = "重置成功"
            self.Flag = True





