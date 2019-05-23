import os, sys, time, signal
from multiprocessing import Process
from socket import *
from e_dictionary.operation_db import *


HOST = '0.0.0.0'
PORT = 12345
ADD = (HOST, PORT)


class Server:
    """
    单词查询软件服务器端
    """
    def __init__(self):
        self.socket = socket()
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(ADD)
        self.socket.listen(3)
        self.db = DataBase()

    def main(self):
        """
        主进程
        :return:
        """
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        print('Listen to port {}'.format(PORT))
        while True:
            try:
                c, addr = self.socket.accept()
                print('{}连接'.format(c.getpeername()))
            except KeyboardInterrupt:
                self.socket.close()
                self.db.close()
                sys.exit('退出程序')
            except Exception as e:
                print(e)
                continue

            p = Process(target=self.do_request, args=(c,))
            p.daemon = True
            p.start()

    def do_request(self, c):
        """
        处理客户端请求
        :param c:
        :return:
        """
        self.db.create_cursor()
        while True:
            data = c.recv(1024).decode()
            msg = data.split(' ')
            if not data:
                print('{}断开连接'.format(c.getpeername()))
                break
            elif msg[0] == 'R':
                self.registered(c, msg[1], msg[2], msg[3])
                print('{}执行注册操作'.format(c.getpeername))
            elif msg[0] == 'L':
                self.login(c, msg[1], msg[2])
                print('{}执行登录操作'.format(c.getpeername))
            elif msg[0] == 'C':
                self.rest(c, msg[1], msg[2])
                print('{}执行重置密码操作'.format(c.getpeername))

    def find_history(self):
        pass

    def find_words(self):
        pass

    def login(self, c, username, password):
        """
        登录
        :param c:
        :param username:
        :param password:
        :return:
        """
        l = self.db.login(username, password)
        if l == 'ok':
            c.send('ok'.encode())
        else:
            c.send(l.encode())

    def registered(self, c, username, password, tell):
        """
        注册
        :param c:
        :param username:
        :param password:
        :param tell:
        :return:
        """
        if self.db.registered(username, password, tell):
            c.send('ok'.encode())
        else:
            c.send('用户名已存在'.encode())

    def rest(self, c, username, tell):
        """
        重置密码
        :param c:
        :param username:
        :param tell:
        :return:
        """
        l = self.db.rest(username, tell)
        if l:
            c.send('ok'.encode())
            psd = c.recv(1024).decode()
            if self.db.updata(username, tell, psd):
                c.send('重置密码成功'.encode())
            else:
                c.send('重置密码失败'.encode())
        else:
            c.send('用户信息不匹配'.encode())


if __name__ == '__main__':
    s = Server()
    s.main()
