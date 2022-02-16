import os
import sys
import time
import base64
import threading
from PyQt5.QtCore import Qt, QUrl
from client import Client
from PyQt5 import QtCore, QtGui, QtWidgets
from audio import *
from PyQt5.QtGui import QImage, QTextDocument

class loginWindow(QtWidgets.QDialog):
    '''
    The login UI
    '''
    def __init__(self):
        super(loginWindow, self).__init__()

        self.setObjectName("LoginWindow")
        self.setStyleSheet("#LoginWindow{border-image:url(./images/style/loginground.jpg);}")
        self.setWindowIcon(QtGui.QIcon("./images/style/icon.png"))
        self.setWindowTitle("FreeChat")
        self.resize(500, 400)

        self.loginButton = QtWidgets.QPushButton(self)      #登录按钮
        self.loginButton.setGeometry(QtCore.QRect(230, 250, 100, 35))
        self.loginButton.setObjectName("login")
        self.loginButton.clicked.connect(self.loginButtonClicked)
        self.loginButton.setText("登录")

        self.registerButton = QtWidgets.QPushButton(self)   #注册按钮
        self.registerButton.setGeometry(QtCore.QRect(120, 250, 100, 35))
        self.registerButton.setObjectName("register")
        self.registerButton.setCursor(Qt.PointingHandCursor)
        self.registerButton.clicked.connect(self.registerButtonClicked)
        self.registerButton.setText("注册")

        self.userName = QtWidgets.QLineEdit(self)       #账号
        self.userName.setGeometry(QtCore.QRect(118, 140, 220, 28))
        self.userName.setObjectName("username")
        self.userName.setPlaceholderText("请输入账号")
        self.userName.setMaxLength(20)
        
        self.password = QtWidgets.QLineEdit(self)       #密码
        self.password.setGeometry(QtCore.QRect(118, 170, 220, 28))
        self.password.setObjectName("password")
        self.password.setPlaceholderText("请输入密码")
        self.password.setMaxLength(20)
        self.password.setEchoMode(self.password.Password)

        self.constuserName = QtWidgets.QLineEdit(self)      #文本输入框前的提示
        self.constuserName.setGeometry(QtCore.QRect(42, 140, 60, 28))
        self.constuserName.setStyleSheet("background:transparent;border:none;")
        self.constuserName.setReadOnly(True)
        self.constuserName.setText("账号：")

        self.constpassword = QtWidgets.QLineEdit(self)
        self.constpassword.setGeometry(QtCore.QRect(42, 170, 60, 28))
        self.constpassword.setStyleSheet("background:transparent;border:none;")
        self.constpassword.setReadOnly(True)
        self.constpassword.setText("密码：")

        self.loginError = QtWidgets.QLineEdit(self)         #登录信息提示框
        self.loginError.setGeometry(QtCore.QRect(118, 70, 220, 28))
        self.loginError.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.loginError.setAlignment(QtCore.Qt.AlignCenter)
        self.loginError.setReadOnly(True)
        self.loginError.setText("登录即可加入群聊!")

        QtCore.QMetaObject.connectSlotsByName(self)

    def loginButtonClicked(self):
        '''
        The event of login button clicked
        '''
        Username = self.userName.text()
        Password = self.password.text()
        if len(Username) == 0 or len(Password) == 0:
            self.loginError.setText("您还没有输入账号或密码")
        else:
            client.login(Username, Password)
            while client.loginBack == None:
                pass
            if client.loginBack["info"] == "loginSucc":
                self.loginError.setStyleSheet("border:none;")
                self.loginError.setText("登陆成功")     
                self.chatWindow = chatWindow(Username)      #登录成功，调出聊天界面
                self.chatWindow.show()
                self.chatWindow.main()
                self.close()
            elif client.loginBack["info"] == "loginFail":
                self.loginError.setText("账号或密码错误")
            else:
                self.loginError.setText("该账号已经登录")
            client.loginBack = None

    def registerButtonClicked(self):
        '''
        The event of register button clicked
        '''
        self.registerWindow = registerWindow()
        self.registerWindow.show()

class registerWindow(QtWidgets.QDialog):
    """
    The register UI
    """
    def __init__(self):
        super(registerWindow, self).__init__()

        self.setObjectName("registerWindow")
        self.setWindowIcon(QtGui.QIcon("./images/style/icon.png"))
        self.resize(360, 330)
        self.setWindowTitle("注册账号")

        self.userName = QtWidgets.QLineEdit(self)       #用户名
        self.userName.setGeometry(QtCore.QRect(118, 80, 220, 28))
        self.userName.setObjectName("username")
        self.userName.setPlaceholderText("请输入账号")
        self.userName.setMaxLength(20)       

        self.password = QtWidgets.QLineEdit(self)       #密码
        self.password.setGeometry(QtCore.QRect(118, 120, 220, 28))
        self.password.setObjectName("password")
        self.password.setPlaceholderText("请输入密码")
        self.password.setMaxLength(20)
        self.password.setEchoMode(self.password.Password)
    
        self.passwordAgain = QtWidgets.QLineEdit(self)  #密码确认
        self.passwordAgain.setGeometry(QtCore.QRect(118, 160, 220, 28))
        self.passwordAgain.setObjectName("passwordAgain")
        self.passwordAgain.setPlaceholderText("请再次输入密码")
        self.passwordAgain.setMaxLength(20)
        self.passwordAgain.setEchoMode(self.password.Password)

        self.constuserName = QtWidgets.QLineEdit(self)  #文本输入框前的提示
        self.constuserName.setGeometry(QtCore.QRect(30, 80, 95, 28))
        self.constuserName.setStyleSheet("background:transparent;border:none;")
        self.constuserName.setReadOnly(True)
        self.constuserName.setText("输入账号：")
        self.constpassword = QtWidgets.QLineEdit(self)
        self.constpassword.setGeometry(QtCore.QRect(30, 120, 95, 28))
        self.constpassword.setStyleSheet("background:transparent;border:none;")
        self.constpassword.setReadOnly(True)
        self.constpassword.setText("输入密码：")
        self.constpasswordAgain = QtWidgets.QLineEdit(self)
        self.constpasswordAgain.setGeometry(QtCore.QRect(30, 160, 95, 28))
        self.constpasswordAgain.setStyleSheet("background:transparent;border:none;")
        self.constpasswordAgain.setReadOnly(True)
        self.constpasswordAgain.setText("确认密码：")

        self.registerButton = QtWidgets.QPushButton(self)   #注册按钮
        self.registerButton.setGeometry(QtCore.QRect(118, 240, 150, 35))
        self.registerButton.setObjectName("register")
        self.registerButton.clicked.connect(self.registerButtonClicked)
        self.registerButton.setText("注册")

        self.registerError = QtWidgets.QLineEdit(self)      #注册信息提示框
        self.registerError.setGeometry(QtCore.QRect(118, 200, 100, 28))
        self.registerError.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.registerError.setAlignment(QtCore.Qt.AlignCenter)
        self.registerError.setReadOnly(True)
        self.registerError.setText("请填写您的个人信息")
            
        QtCore.QMetaObject.connectSlotsByName(self)

    def registerButtonClicked(self):
        '''
        the event of register button clicked
        '''
        Username = self.userName.text()
        password = self.password.text()
        passwordAgain = self.passwordAgain.text()
        if len(Username) == 0 or len(password) == 0 or len(passwordAgain) == 0:
            self.registerError.setText("您还没有输入账号或密码！")
        elif password != passwordAgain:
            self.registerError.setText("您两次输入的密码不同！")
        else:
            client.register(Username, password)
            while client.registerBack == None:
                pass
            if client.registerBack["info"] == "rgtrSucc":
                self.registerError.setStyleSheet("border:none;")
                self.registerError.setText("注册成功！请返回登录！")
            else:
                self.registerError.setText("该账号已存在！")
            client.registerBack = None

class PrivateChatWindow(QtWidgets.QDialog):
    '''Private chat window UI
    Args:
        Aname: Username
        Bname: Destname
    '''
    def __init__(self,Aname,Bname):
        super(PrivateChatWindow, self).__init__()
        self.Aname = Aname
        self.Bname = Bname
        self.Username = Aname
        self.setupUI()

    def setupUI(self):
        self.setObjectName("FreeChat")
        self.setStyleSheet("#FreeChat{border-image:url(./images/style/loginground.jpg);}")
        self.setWindowIcon(QtGui.QIcon("./images/style/icon.png"))
        self.setWindowTitle("A conversation initiated by "+self.Username)
        self.resize(685, 463)
        
        self.PrivateText = QtWidgets.QTextEdit(self)        #私聊消息框
        self.PrivateText.setGeometry(QtCore.QRect(5, 20, 670, 280))
        self.PrivateText.setObjectName("textRecv")
        self.PrivateText.setAlignment(QtCore.Qt.AlignTop)
        self.PrivateText.setReadOnly(True)

        self.sendText = QtWidgets.QTextEdit(self)           #发送消息的编辑框
        self.sendText.setGeometry(QtCore.QRect(5, 335, 670, 85)) 
        self.sendText.setObjectName("textSend")
        self.sendText.setAlignment(QtCore.Qt.AlignTop)
        
        self.destsend = self.Bname

        self.sendtxtButton = QtWidgets.QPushButton(self)    #发送消息的按钮
        self.sendtxtButton.setGeometry(QtCore.QRect(520, 425, 150, 27))
        self.sendtxtButton.setObjectName("txtsendButton")
        self.sendtxtButton.clicked.connect(self.SendButtonClicked)
        self.sendtxtButton.setText("发送给"+self.Bname)

        self.fileButton = QtWidgets.QPushButton(self)       #发送文件的按钮
        self.fileButton.setGeometry(QtCore.QRect(5, 300, 35, 35))
        self.fileButton.setStyleSheet("border-image:url(./images/style/file.png);")
        self.fileButton.clicked.connect(self.fileButtonClicked)

        self.imageButton = QtWidgets.QPushButton(self)      #发送图片的按钮
        self.imageButton.setGeometry(QtCore.QRect(45, 300, 35, 35))
        self.imageButton.setStyleSheet("border-image:url(./images/style/photo.png);")
        self.imageButton.clicked.connect(self.imageButtonClicked)

        self.emojiButton = QtWidgets.QPushButton(self)      # 发送表情的按钮
        self.emojiButton.setGeometry(QtCore.QRect(85, 300, 35, 35))
        self.emojiButton.setStyleSheet("border-image:url(./images/style/emoji.png);")
        self.emojiButton.clicked.connect(self.emojiButtonClicked)

        self.audioButton = QtWidgets.QPushButton(self)      # 发送语音的按钮
        self.audioButton.setGeometry(QtCore.QRect(125, 300, 35, 35))
        self.audioButton.setStyleSheet("border-image:url(./images/style/audio.png);")
        self.audioButton.clicked.connect(self.audioButtonClicked)

        self.earButton = QtWidgets.QPushButton(self)      # 听取音频的按钮
        self.earButton.setGeometry(QtCore.QRect(165, 300, 35, 35))
        self.earButton.setStyleSheet("border-image:url(./images/style/ear.png);")
        self.earButton.clicked.connect(self.earButtonClicked)

        self.fileselect = QtWidgets.QFileDialog(self)       #文件选择界面
        self.fileselect.setGeometry(QtCore.QRect(248, 341, 500, 62))

        self.emoji = QtWidgets.QTableWidget(self)           #表情列表
        self.emoji.setGeometry(QtCore.QRect(75, 175, 120, 120))
        self.emoji.verticalHeader().setVisible(False)       # 隐藏垂直表头
        self.emoji.horizontalHeader().setVisible(False)     # 隐藏水平表头
        self.emoji.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)   # 隐藏垂直滚动条
        self.emoji.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)     # 隐藏水平滚动条
        self.emoji.setColumnCount(3)
        self.emoji.setRowCount(3)
        for i in range(9):
            icon = QtWidgets.QLabel()
            icon.setMargin(4)
            movie = QtGui.QMovie()
            movie.setScaledSize(QtCore.QSize(30, 30))
            movie.setFileName("./images/emoji/"+str(i)+".gif")
            movie.start()
            icon.setMovie(movie)
            self.emoji.setCellWidget(int(i/3), i%3, icon)
            self.emoji.setColumnWidth(i%3, 40)          # 设置列的宽度
            self.emoji.setRowHeight(int(i/3), 40)       # 设置行的高度
        self.emoji.hide()
        self.emoji.cellClicked.connect(self.emojiClicked)

        QtCore.QMetaObject.connectSlotsByName(self)
   
    def SendButtonClicked(self):
        text = self.sendText.toPlainText()
        if len(text):
            client.send_Msg(text, self.destsend)
            self.sendText.clear()

    def fileButtonClicked(self):
        fileinfo = self.fileselect.getOpenFileName(self, 'OpenFile', "e:/")
        print(fileinfo)
        filepath, filetype = os.path.splitext(fileinfo[0])
        filename = filepath.split("/")[-1]
        if fileinfo[0] != '':
            with open(fileinfo[0], mode='rb') as f:
                r = f.read()
                f.close()
            file_r = base64.encodebytes(r).decode("utf-8")
            client.send_Msg(file_r, self.destsend, filetype, filename)

    def imageButtonClicked(self):
        fileinfo = self.fileselect.getOpenFileName(self,'OpenFile',"e:/","Image files (*.jpg *.gif *.png)")
        print(fileinfo)
        filepath, filetype = os.path.splitext(fileinfo[0])
        filename = filepath.split("/")[-1]
        if fileinfo[0] != '':
            with open(fileinfo[0], mode='rb') as f:
                r = f.read()
                f.close()
            file_r = base64.encodebytes(r).decode("utf-8")
            client.send_Msg(file_r, self.destsend, filetype, filename)

    def emojiButtonClicked(self):
        self.emoji.show()

    def emojiClicked(self, row, column):
        client.send_Msg(row*3+column , self.destsend, "emoji")
        self.emoji.hide()


    def audioButtonClicked(self):
        T = time.strftime('%Y-%m-%d-%H-%M-%S') 
        path = self.Username + "/" + T+".wav"
        record_audio(path,5)
        with open(path, mode='rb') as f:
            r = f.read()
            f.close()
        file_r = base64.encodebytes(r).decode("utf-8")
        client.send_Msg(file_r, self.destsend, ".wav", T)

    def earButtonClicked(self):
        names = os.listdir(self.Username)
        ls = []
        for name in names:
            if name[-3:] == "wav":
                ls.append(name)
        for i in ls:
            play_audio(self.Username+"/"+i)
            os.remove(self.Username+"/"+i)
    
    def recv(self):
        while True:
            while len(client.usermsg):
                msg_recv = client.usermsg.pop()
                msgtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(msg_recv["time"]))
                if msg_recv["destname"] == "all":
                    client.usermsg.append(msg_recv)
                    time.sleep(0.0001)
                    continue
                
                #文本信息
                if msg_recv["mtype"] == "msg": 
                    msg_recv["msg"] = msg_recv["msg"].replace("\n","\n ")
                    if msg_recv["name"] == self.Username:       #从本地发送的消息打印
                        #self.PrivateText.moveCursor(QtGui.QTextCursor.End)
                        self.PrivateText.setTextColor(Qt.green)
                        self.PrivateText.insertPlainText(" " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        self.PrivateText.setTextColor(Qt.black)
                        self.PrivateText.insertPlainText(msg_recv["msg"] + "\n")                       
                    elif msg_recv["destname"] == self.Username:        #本地接收到的消息打印
                        #self.PrivateText.moveCursor(QtGui.QTextCursor.End)
                        self.PrivateText.setTextColor(Qt.blue)
                        self.PrivateText.insertPlainText(" " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        self.PrivateText.setTextColor(Qt.black)
                        self.PrivateText.insertPlainText(msg_recv["msg"] + "\n")

                #表情信息
                elif msg_recv["mtype"] == "emoji":
                    if msg_recv["name"] == self.Username:  # 从本地发送的消息打印
                        #self.PrivateText.moveCursor(QtGui.QTextCursor.End)
                        self.PrivateText.setTextColor(Qt.green)
                        self.PrivateText.insertPlainText(
                            " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./images/emoji/"+ str(msg_recv["msg"]) +".gif"
                        tcursor = self.PrivateText.textCursor()
                        img = QtGui.QTextImageFormat()
                        img.setName(path)
                        img.setHeight(28)
                        img.setWidth(28)
                        tcursor.insertImage(img)
                        self.PrivateText.insertPlainText("\n")
                    elif msg_recv["destname"] == self.Username:  # 本地接收到的消息打印
                        self.PrivateText.moveCursor(QtGui.QTextCursor.End)
                        self.PrivateText.setTextColor(Qt.blue)
                        self.PrivateText.insertPlainText(
                            " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./images/emoji/"+ str(msg_recv["msg"]) +".gif"
                        tcursor = self.PrivateText.textCursor()
                        img = QtGui.QTextImageFormat()
                        img.setName(path)
                        img.setHeight(28)
                        img.setWidth(28)
                        tcursor.insertImage(img)
                        self.PrivateText.insertPlainText("\n")

                #文件信息
                else:
                    if msg_recv["name"] == self.Username:  # 从本地发送的消息打印
                        #self.PrivateText.moveCursor(QtGui.QTextCursor.End)
                        self.PrivateText.setTextColor(Qt.green)
                        self.PrivateText.insertPlainText(" " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                        with open(path,"wb") as f:
                            f.write(base64.b64decode(msg_recv["msg"]))
                            f.close()
                        if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                            tcursor = self.PrivateText.textCursor()
                            img = QtGui.QTextImageFormat()
                            img.setName(path)
                            img.setHeight(100)
                            img.setWidth(100)
                            tcursor.insertImage(img)
                        elif msg_recv["mtype"] == ".wav":
                            self.PrivateText.insertPlainText("您发送了一条语言消息" )                    
                        else:
                            self.PrivateText.insertPlainText("您发送的文件已保存在：" + path)
                        self.PrivateText.insertPlainText("\n")
                    elif msg_recv["destname"] == self.Username:  # 本地接收到的消息打印
                        #self.PrivateText.moveCursor(QtGui.QTextCursor.End)
                        self.PrivateText.setTextColor(Qt.blue)
                        self.PrivateText.insertPlainText(" " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                        with open(path, "wb") as f:
                            f.write(base64.b64decode(msg_recv["msg"]))
                            f.close()
                        if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                            tcursor = self.PrivateText.textCursor()
                            img = QtGui.QTextImageFormat()
                            img.setName(path)
                            img.setHeight(100)
                            img.setWidth(100)
                            tcursor.insertImage(img)
                        elif msg_recv["mtype"] == ".wav":
                            self.PrivateText.insertPlainText("您收到了一条语言消息" )                            
                        else:
                            self.PrivateText.insertPlainText("您收到的文件已保存在：" + path)
                        self.PrivateText.insertPlainText("\n")
                        
    def main(self):
        func = threading.Thread(target=self.recv)
        func.start()

class chatWindow(QtWidgets.QDialog):
    """
    Group chat window UI
    """
    def __init__(self, name):
        self.Username = name
        self.Destname = ''
        super(chatWindow, self).__init__()
        self.setupUi()
        try:
            os.mkdir(self.Username)         #创建对应的文件夹
        except FileExistsError:
            pass

    def setupUi(self):

        self.setObjectName("MyChat")
        self.setStyleSheet("#MyChat{border-image:url(./images/style/loginground.jpg);}")
        self.setWindowIcon(QtGui.QIcon("./images/style/icon.png"))
        self.resize(810, 440)

        self.grprecvText = QtWidgets.QTextBrowser(self)        #群聊消息框
        self.grprecvText.setGeometry(QtCore.QRect(5, 20, 670, 275))
        self.grprecvText.setObjectName("textRecv")
        self.grprecvText.setAlignment(QtCore.Qt.AlignTop)
        self.grprecvText.setReadOnly(True)

        self.sendText = QtWidgets.QTextEdit(self)           #发送消息的编辑框
        self.sendText.setGeometry(QtCore.QRect(5, 340, 670, 90)) #
        self.sendText.setObjectName("textSend")
        self.sendText.setAlignment(QtCore.Qt.AlignTop)
        self.destsend = 'all'

        self.sendtxtButton = QtWidgets.QPushButton(self)    #发送消息的按钮
        self.sendtxtButton.setGeometry(QtCore.QRect(700, 350, 65, 27))
        self.sendtxtButton.setObjectName("txtsendButton")
        self.sendtxtButton.clicked.connect(self.txtsendButtonClicked)
        self.sendtxtButton.setText("发送")

        self.friendlistHeader = QtWidgets.QLineEdit(self)   # 在线好友列表头
        self.friendlistHeader.setGeometry(QtCore.QRect(675, 20, 125, 30))
        self.friendlistHeader.setObjectName("friendlistHeader")
        self.friendlistHeader.setAlignment(QtCore.Qt.AlignTop)
        self.friendlistHeader.setReadOnly(True)
        self.friendlistHeader.setText("在线好友")

        self.friendlist = QtWidgets.QListWidget(self)       #在线好友列表
        self.friendlist.setGeometry(QtCore.QRect(675, 45, 125, 250))
        self.friendlist.setObjectName("friendlist")
        self.friendlist.doubleClicked.connect(self.friendlistDoubleClicked)
        self.friendlist.addItems(client.userlist)

        self.fileButton = QtWidgets.QPushButton(self)       #发送文件的按钮
        self.fileButton.setGeometry(QtCore.QRect(5, 300, 35, 35))
        self.fileButton.setStyleSheet("border-image:url(./images/style/file.png);")
        self.fileButton.clicked.connect(self.fileButtonClicked)

        self.imageButton = QtWidgets.QPushButton(self)      #发送图片的按钮
        self.imageButton.setGeometry(QtCore.QRect(45, 300, 35, 35))
        self.imageButton.setStyleSheet("border-image:url(./images/style/photo.png);")
        self.imageButton.clicked.connect(self.imageButtonClicked)

        self.emojiButton = QtWidgets.QPushButton(self)      # 发送表情的按钮
        self.emojiButton.setGeometry(QtCore.QRect(85, 300, 35, 35))
        self.emojiButton.setStyleSheet("border-image:url(./images/style/emoji.png);")
        self.emojiButton.clicked.connect(self.emojiButtonClicked)

        self.audioButton = QtWidgets.QPushButton(self)      # 发送语音的按钮
        self.audioButton.setGeometry(QtCore.QRect(125, 300, 35, 35))
        self.audioButton.setStyleSheet("border-image:url(./images/style/audio.png);")
        self.audioButton.clicked.connect(self.audioButtonClicked)

        self.earButton = QtWidgets.QPushButton(self)      # 听取音频的按钮
        self.earButton.setGeometry(QtCore.QRect(165, 300, 35, 35))
        self.earButton.setStyleSheet("border-image:url(./images/style/ear.png);")
        self.earButton.clicked.connect(self.earButtonClicked)

        self.fileselect = QtWidgets.QFileDialog(self)       #文件选择界面
        self.fileselect.setGeometry(QtCore.QRect(248, 341, 500, 62))

        self.emoji = QtWidgets.QTableWidget(self)           #表情列表
        self.emoji.setGeometry(QtCore.QRect(75, 175, 120, 120))
        self.emoji.verticalHeader().setVisible(False)       # 隐藏垂直表头
        self.emoji.horizontalHeader().setVisible(False)     # 隐藏水平表头
        self.emoji.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)   # 隐藏垂直滚动条
        self.emoji.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)     # 隐藏水平滚动条
        self.emoji.setColumnCount(3)
        self.emoji.setRowCount(3)
        for i in range(9):
            icon = QtWidgets.QLabel()
            icon.setMargin(4)
            movie = QtGui.QMovie()
            movie.setScaledSize(QtCore.QSize(30, 30))
            movie.setFileName("./images/emoji/"+str(i)+".gif")
            movie.start()
            icon.setMovie(movie)
            self.emoji.setCellWidget(int(i/3), i%3, icon)
            self.emoji.setColumnWidth(i%3, 40)          # 设置列的宽度
            self.emoji.setRowHeight(int(i/3), 40)       # 设置行的高度
        self.emoji.hide()
        self.emoji.cellClicked.connect(self.emojiClicked)

        QtCore.QMetaObject.connectSlotsByName(self)
   
    def txtsendButtonClicked(self):
        '''
        the event of send button clicked
        '''
        text = self.sendText.toPlainText()
        if len(text):
            client.send_Msg(text, self.destsend)
            self.sendText.clear()

    def friendlistDoubleClicked(self):
        '''
        double click the friend to start private chat
        '''
        name = self.friendlist.currentItem().text()      #聊天对象
        if name == self.Username:
            return
        self.PrivateChatWindow = PrivateChatWindow(self.Username,name)      #登录成功，调出聊天界面
        self.PrivateChatWindow.show()
        self.PrivateChatWindow.main()

    def fileButtonClicked(self):
        fileinfo = self.fileselect.getOpenFileName(self, 'OpenFile', "e:/")
        filepath, filetype = os.path.splitext(fileinfo[0])
        filename = filepath.split("/")[-1]
        if fileinfo[0] != '':
            with open(fileinfo[0], mode='rb') as f:
                r = f.read()
                f.close()
            file_r = base64.encodebytes(r).decode("utf-8")
            client.send_Msg(file_r, self.destsend, filetype, filename)

    def imageButtonClicked(self):
        fileinfo = self.fileselect.getOpenFileName(self,'OpenFile',"e:/","Image files (*.jpg *.gif *.png)")
        filepath, filetype = os.path.splitext(fileinfo[0])
        filename = filepath.split("/")[-1]
        if fileinfo[0] != '':
            with open(fileinfo[0], mode='rb') as f:
                r = f.read()
                f.close()
            file_r = base64.encodebytes(r).decode("utf-8")
            client.send_Msg(file_r, self.destsend, filetype, filename)

    def emojiButtonClicked(self):
        if self.emoji.isVisible():
            self.emoji.hide()
        else:
            self.emoji.show()

    def emojiClicked(self, row, column):
        client.send_Msg(row*3+column , self.destsend, "emoji")
        self.emoji.hide()

    def audioButtonClicked(self):
        T = time.strftime('%Y-%m-%d-%H-%M-%S') 
        path = self.Username + "/" + T+".wav"
        record_audio(path,5)
        with open(path, mode='rb') as f:
            r = f.read()
            f.close()
        file_r = base64.encodebytes(r).decode("utf-8")
        client.send_Msg(file_r, self.destsend, ".wav", T)

    def earButtonClicked(self):
        names = os.listdir(self.Username)
        ls = []
        for name in names:
            if name[-3:] == "wav":
                ls.append(name)
        for i in ls:
            play_audio(self.Username+"/"+i)
            os.remove(self.Username+"/"+i)

    def recv(self):
        while True:
            while len(client.usermsg):
                msg_recv = client.usermsg.pop()
                msgtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(msg_recv["time"]))
                if msg_recv["destname"] != "all":
                    client.usermsg.append(msg_recv)
                    time.sleep(0.0001)
                    continue
                 
                #文本信息
                if msg_recv["mtype"] == "msg":
                    msg_recv["msg"] = msg_recv["msg"].replace("\n","\n  ")
                    if (msg_recv["name"] == self.Username) & (msg_recv["destname"] == "all"):       #从本地发送的消息打印                   
                        self.grprecvText.setTextColor(Qt.green)
                        self.grprecvText.insertPlainText(" " +msg_recv["name"] + "  " + msgtime+"\n")
                        self.grprecvText.setTextColor(Qt.black)
                        self.grprecvText.insertPlainText(" " +msg_recv["msg"] + "\n")
                        self.grprecvText.ensureCursorVisible()
                        #cursor = self.grprecvText.textCursor()
                        #cursor.movePosition(QtGui.QTextCursor.End)
                        
                    #elif msg_recv["destname"] == "all":        #本地接收到的消息打印
                    else:
                        #cursor = self.grprecvText.textCursor()
                        #cursor.movePosition(QtGui.QTextCursor.End)
                        self.grprecvText.setTextColor(Qt.blue)
                        self.grprecvText.insertPlainText(
                            " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        self.grprecvText.setTextColor(Qt.black)
                        self.grprecvText.insertPlainText(msg_recv["msg"] + "\n")

                #表情信息
                elif msg_recv["mtype"] == "emoji":
                    if (msg_recv["name"] == self.Username) & (msg_recv["destname"] == "all"):  # 从本地发送的消息打印
                        #self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                        self.grprecvText.setTextColor(Qt.green)
                        self.grprecvText.insertPlainText(" " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./images/emoji/"+ str(msg_recv["msg"]) +".gif"
                        tcursor = self.grprecvText.textCursor()
                        # cursor = self.textEdit.textCursor()
                        # document = self.textEdit.document()
                        # document.addResource(QTextDocument.ImageResource, QUrl("image"), image)
                        # cursor.insertImage("image")
                        # image = QImage(path)
                        # document = self.grprecvText.document()
                        # document.addResource(QTextDocument.ImageResource,QUrl("image"), image)
                        img = QtGui.QTextImageFormat()
                        img.setName(path)
                        img.setHeight(28)
                        img.setWidth(28)
                        # src = "<img src="+path+" />"
                        # self.grprecvText.append(src)
                        tcursor.insertImage(img)
                        self.grprecvText.insertPlainText("\n")
        
                    elif msg_recv["destname"] == "all":  # 本地接收到的消息打印
                        self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                        self.grprecvText.setTextColor(Qt.blue)
                        self.grprecvText.insertPlainText(" " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./images/emoji/"+ str(msg_recv["msg"]) +".gif"
                        tcursor = self.grprecvText.textCursor()
                        img = QtGui.QTextImageFormat()
                        img.setName(path)
                        img.setHeight(28)
                        img.setWidth(28)
                        tcursor.insertImage(img)
                        self.grprecvText.insertPlainText("\n")

                #文件和语音信息
                else:
                    if (msg_recv["name"] == self.Username) & (msg_recv["destname"] == "all"):  # 从本地发送的消息打印
                        self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                        self.grprecvText.setTextColor(Qt.green)
                        self.grprecvText.insertPlainText(
                            " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                        with open(path,"wb") as f:
                            f.write(base64.b64decode(msg_recv["msg"]))
                            f.close()
                        tcursor = self.grprecvText.textCursor()
                        
                        if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                            img = QtGui.QTextImageFormat()
                            img.setName(path)
                            img.setHeight(100)
                            img.setWidth(100)
                            tcursor.insertImage(img)
                        elif msg_recv["mtype"] == ".wav":
                            self.grprecvText.insertPlainText("您发送了一条语言消息" )
                        else:
                            self.grprecvText.insertPlainText("发送的文件已保存在：" + path)
                        self.grprecvText.insertPlainText("\n")
        
                    elif msg_recv["destname"] == "all":  # 本地接收到的消息打印
                        #self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                        self.grprecvText.setTextColor(Qt.blue)
                        self.grprecvText.insertPlainText(
                            " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                        path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                        with open(path, "wb") as f:
                            f.write(base64.b64decode(msg_recv["msg"]))
                            f.close()                 
                        if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                            tcursor = self.grprecvText.textCursor() 
                            img = QtGui.QTextImageFormat()
                            img.setName(path)
                            img.setHeight(100)
                            img.setWidth(100)
                            tcursor.insertImage(img)
                        elif msg_recv["mtype"] == ".wav":
                            self.grprecvText.insertPlainText("您收到了一条语言消息" )
                        else:
                            self.grprecvText.insertPlainText("接收的文件已保存在：" + path)
                        self.grprecvText.insertPlainText("\n")
                        
            while len(client.sysmsg):
                msg_recv = client.sysmsg.pop()
                if msg_recv["info"] == "userlogin":
                    if msg_recv["name"] not in client.userlist:
                        client.userlist.append(msg_recv["name"])
                        self.friendlist.clear()
                        self.friendlist.addItems(client.userlist)
                elif msg_recv["info"] == "userexit":
                    if msg_recv["name"] in client.userlist:
                        client.userlist.remove(msg_recv["name"])
                        self.friendlist.clear()
                        self.friendlist.addItems(client.userlist)
                self.grprecvText.setTextColor(Qt.gray)
                self.grprecvText.insertPlainText(" "+msg_recv["msg"]+"\n")

    def main(self):
        func1 = threading.Thread(target=self.recv)
        func1.start()

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv) 
    client = Client(addr="localhost", port=14396)
    client.main()

    login = loginWindow()
    login.show()

    sys.exit(app.exec_())

