import time
import queue
import socket
import threading

class Client(object):
    def __init__(self, addr="127.0.0.1", port=9999):
        """
        The class of client

        Args:
            addr: the client address
            port: the port client uses, the default value is 9999
        """
        self.addr = addr
        self.port = port
        self.username = None
        self.queue = queue.Queue()
        self.status = True
        self.loginStatus = False
        self.loginBack = None
        self.registerBack = None
        self.userlist = []
        self.usermsg = []
        self.sysmsg = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #创建TCP Socket

        try:
            self.s.connect((self.addr, self.port))
            self.s.settimeout(0.1)
        except socket.error as err:
            if err.errno == 10061:
                print("Connection with {addr}:{port} refused".format(addr=self.addr, port=self.port))
                return
            else:
                raise
        else:
            print("initial successfully!")

    def register(self, name, password):
        """
        A function to sent register message

        Args:
            name: username
            password: the password
        """
        self.s.send(str({"type": "register",
                        "name": name,
                        "password": password,
                        "time": time.time()}).encode())

    def login(self, name, password):
        """
        A function to sent login message

        Args:
            name: username
            password: the password
        """
        self.username = name
        self.s.send(str({"type": "login",
                        "name": name,
                        "password": password,
                        "time": time.time()}).encode())

    def send_Msg(self, msg_send, destname, type = "msg", fname = ""):
        """
        The function to send message

        Args:
            msg_send: the message to send
            destname: the destination
            type: the kind of message to recognize emoji etc., default value is msg
        """
        a = str({"type": "usermsg",
                "mtype": type,
                "destname": destname,
                "fname": fname,
                "name": self.username,
                "time": time.time(),
                "msg": msg_send}).encode()
        constlen = len(a)

        mes = str({"type": "msglen",
                "destname": destname,
                "name": self.username,
                "len": constlen}).encode()
        self.s.send(mes)
        time.sleep(0.01)
        self.s.send(a)
        print("new information sent")

    def receive_msg(self):
        """
        A funtion to recevie message
        """
        while self.status:
            try:
                msg_recv = eval(self.s.recv(1024))
            except socket.timeout:
                pass
            except:
                print("other error")
            else:
                if msg_recv["type"] == "msglen":
                    self.queue.put(msg_recv)
                    length = msg_recv["len"]
                    mlen = 0
                    while msg_recv["type"] != "usermsg":
                        try:
                            msg_recv = "".encode()

                            while mlen < length:
                                try:
                                    msg_recv_ = self.s.recv(length)
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
                        except socket.error as err:
                            if err.errno == 10053:
                                print("Software caused connection abort ")
                                self.status = False
                    self.queue.put(msg_recv)
                    print("new information received")
                else:
                    self.queue.put(msg_recv)
                    print("new information received")       

    def handle_msg(self):
        """
        A function to handle message
        """
        while True:
            msg = self.queue.get()
            
            if msg["type"] == "loginBack":
                self.loginBack = msg
                if msg["info"] == "loginSucc":
                    self.userlist = msg["userlist"]
            elif msg["type"] == "rgtrBack":
                self.registerBack = msg
            elif msg["type"] == "usermsg":
                self.usermsg.append(msg)
            elif msg["type"] == "sysmsg":
                self.sysmsg.append(msg)

    def main(self):
        """
        the main function
        """
        receive_func = threading.Thread(target=self.receive_msg)
        handle_func = threading.Thread(target=self.handle_msg)
        receive_func.start()
        handle_func.start()

    def __del__(self):
        self.s.close()

if __name__ == '__main__':
    client = Client(addr="127.0.0.1", port=14396)
    client.main()
    client.login("0", "0")

