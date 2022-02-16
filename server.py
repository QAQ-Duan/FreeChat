import time
import queue
import socket
import sqlite3
import threading

class Server(object):
    def __init__(self, addr="localhost", port=12345):
        self.addr = addr
        self.port = port

        self.connections = []
        self.name = {}
        self.nametoconn = {}
        self.userlist = []
        self.queue = queue.Queue()

        self.dbconn = sqlite3.connect('UserInfo.db')
        self.dbcursor = self.dbconn.cursor()
        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS USERINFO
               (USERNAME    VARCHAR(20) PRIMARY KEY     NOT NULL,
                PASSWORD    VARCHAR(20)                 NOT NULL,
                LASTLOGIN   VARCHAR(50)                 NOT NULL,
                STATUS      INT(1)                      NOT NULL
                               );''')
        self.dbcursor.execute("UPDATE USERINFO set STATUS = 0")
        self.dbconn.commit()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #创建TCP Socket
        self.s.bind((self.addr, self.port))                                 #将套接字绑定到地址
        print("Initial Successfully!")

    def portlisten(self):
        """
        A function to listen TCP connect
        """
        self.s.listen(10)                           #监听TCP传入连接
        while True:
            conn, address = self.s.accept()         #接受TCP连接并返回（conn,address）
            conn.settimeout(0.000001)
            add = address[0] + ":" + str(address[1])
            print("address is "+address[0]+" the port is "+str(address[1]))
            self.connections.append(conn)           #存储已建立的连接
            self.name[add] = add

    def msg_queue(self):
        """
        Create the message queue
        """
        while True:
            for c in self.connections:
                try:
                    msg_recv = eval(c.recv(1024))
                    print("message received, the message is below")
                    print(msg_recv)
                except socket.timeout:
                    continue
                except SyntaxError:
                    pass
                except socket.error as err:     #10053 – Software caused connection abort //10054 – connection reset by peer
                    if err.errno == 10053 or err.errno == 10054:
                        self.remove_connection(c)
                except ValueError:
                    pass
                else:
                    addr = c.getpeername()
                    self.queue.put((addr, msg_recv, c))
                    if msg_recv["type"] == "msglen":
                        length = msg_recv["len"]
                        time.sleep(length * 0.0000001)
                        mlen = 0
                        while msg_recv["type"] != "usermsg":
                            try:
                                msg_recv = "".encode()
                                while mlen < length:        #直至收到事先给予的长度才停下
                                    try:
                                        msg_recv_ = c.recv(length)
                                        print(msg_recv_)
                                        msg_recv = msg_recv + msg_recv_
                                        mlen = mlen + len(msg_recv_)
                                        msg_recv = eval(msg_recv)
                                        time.sleep(length * 0.00000001)
                                    except socket.timeout:
                                        continue
                                    except SyntaxError:
                                        continue
                                    else:
                                        break
                            except socket.timeout:
                                continue
                            except socket.error as err:  # 10053 – Software caused connection abort //10054 – connection reset by peer
                                if err.errno == 10053 or err.errno == 10054:
                                    self.remove_connection(c)
                            except ValueError:
                                pass
                        self.queue.put((addr, msg_recv, c))

    def login(self, msg_recv, addr):
        """
        A function to address the login message

        Arg:
            msg_recv: the message received
            addr: the user address
        """
        Username = msg_recv["name"]
        self.dbcursor.execute("SELECT * from USERINFO where USERNAME = \"{Uname}\"".format(Uname = Username))      #通过用户名检索出对应的用户实体
        Userinfo = self.dbcursor.fetchone()

        if Userinfo == None or Userinfo[1] != msg_recv["password"]:        #用户不存在或密码错误
            flag = False
            back = {"type": "loginBack",
                    "info": "loginFail"}
        elif Userinfo[3] == 1:
            flag = False
            back = {"type": "loginBack",
                    "info": "loginAlready"}
        else:
            flag = True
            address = addr[0] + ":" + str(addr[1])

            self.name[address] = Username
            self.userlist.append(Username)
            self.lastlogintime = Userinfo[2]
            self.dbcursor.execute("UPDATE USERINFO set LASTLOGIN = {logintime}, STATUS = 1 where USERNAME=\"{Uname}\"".format(
                logintime = time.time(),           #time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(msg_recv["time"])),
                Uname = Username))
            self.dbconn.commit()
            back = {"type": "loginBack",
                    "info": "loginSucc",
                    "userlist": self.userlist}
            forward = {"type": "sysmsg",
                       "info": "userlogin",
                       "name": Username,
                       "time": time.time(),
                       "msg": "{name} come in the group chat!".format(name=Username)}

        for c in self.connections:
            c_addr = c.getpeername()
            if c_addr == addr:
                if flag:
                    self.nametoconn[self.name[address]] = c
                c.send(str(back).encode())
            elif flag:
                c.send(str(forward).encode())

    def register(self, msg_recv, addr):
        """
        A function to address register message

        Args
            msg_recv: the message received
            addr: the user address
        """
        Username = msg_recv["name"]
        self.dbcursor.execute("SELECT * from USERINFO where USERNAME=\"{Uname}\"".format(Uname = Username))  # 通过用户名检索出对应的用户实体
        Userinfo = self.dbcursor.fetchone()

        if Userinfo == None:        # 用户不存在
            self.dbcursor.execute("INSERT INTO USERINFO (USERNAME, PASSWORD, LASTLOGIN, STATUS) \
            VALUES (\"{Uname}\", \"{Passwd}\", \"Never\", 0)".format(Uname = Username, Passwd = msg_recv["password"]))
            self.dbconn.commit()

            self.name[addr] = Username
            self.lastlogintime = "Never"
            back = {"type": "rgtrBack",
                    "info": "rgtrSucc"}
        else:
            back = {"type": "rgtrBack",
                    "info": "rgtrFail"}

        for c in self.connections:
            c_addr = c.getpeername()
            if c_addr == addr:
                c.send(str(back).encode())

    def remove_connection(self, conn):
        '''
        A function to address the quit message
        Arg:
            conn: the connection to delete
        '''
        try:
            self.connections.remove(conn)
        except ValueError:
            pass
        address = conn.getpeername()
        addr = address[0] + ":" + str(address[1])
        Username = self.name[addr]
        self.name.pop(addr)     #从用户列表中移除
        if Username in self.userlist:
            self.userlist.remove(Username)
        dbconn1 = sqlite3.connect('userinfo.db')
        dbcursor1 = dbconn1.cursor()
        dbcursor1.execute("UPDATE USERINFO set STATUS=0 where USERNAME=\"{Uname}\"".format(Uname=Username))
        dbconn1.commit()
        back = {"type": "sysmsg",
                "info": "userexit",
                "name": Username,
                "time": time.time(),
                "msg": "{name} leave the chatroom".format(name=Username)}
        for c in self.connections:
            c.send(str(back).encode())

    def msg_forward(self, msg_forward):
        """
        A function to forward message

        Args:
            msg_forward: the message to forward
        """
        #address = addr[0] + ":" + str(addr[1])
        if msg_forward["destname"] == "all":
            for c in self.connections:
                print("new information forward to group")
                c.send(str(msg_forward).encode())
        else:
            self.nametoconn[msg_forward["destname"]].send(str(msg_forward).encode())
            self.nametoconn[msg_forward["name"]].send(str(msg_forward).encode())
            print("new information forward to "+msg_forward["destname"])

    def run(self):
        """
        Run the server!
        """
        func1 = threading.Thread(target=self.portlisten)
        func2 = threading.Thread(target=self.msg_queue)
        func1.start()
        func2.start()
        while True:
            time.sleep(0.001)
            if self.queue.empty():
                continue
            addr, msg, conn = self.queue.get()
            if msg["type"] == "login":
                self.login(msg, addr)
            elif msg["type"] in ("usermsg", "msglen"):
                self.msg_forward(msg)
            elif msg["type"] == "register":
                self.register(msg, addr)
                
    def __del__(self):
        self.s.close()
        self.dbconn.close()

if __name__ == '__main__':
    server = Server(addr="127.0.0.1", port=14396)
    server.run()

    

