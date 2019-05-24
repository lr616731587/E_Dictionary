"""
客户端
"""
import sys
import signal

from multiprocessing import Process
from socket import *
from e_dictionary.operation_db import *
from e_dictionary.settings import *


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
            if not data or msg[0] == 'E':
                print('{}断开连接'.format(c.getpeername()))
                c.close()
                sys.exit('客户端退出')
            elif msg[0] == 'R':
                print('{}执行注册操作'.format(c.getpeername()))
                self.registered(c, msg[1], msg[2], msg[3])
            elif msg[0] == 'L':
                print('{}执行登录操作'.format(c.getpeername()))
                self.login(c, msg[1], msg[2])
            elif msg[0] == 'C':
                print('{}执行重置密码操作'.format(c.getpeername()))
                self.rest(c, msg[1], msg[2])

    def find_history(self, c, username):
        """
        查询历史记录
        :param c:
        :param username:
        :return:
        """
        h = self.db.find_history(username)
        if not h:
            c.send('暂无历史记录'.encode())
            return
        for i in h:
            msg = '%s\t%s\t%s' % i
            time.sleep(0.1)
            c.send(msg.encode())
        time.sleep(0.1)
        c.send(b'##')  # 发送终止条件

    def find_words(self, c, word, username):
        """
        查询单词
        :param c:
        :param word:
        :param username:
        :return:
        """
        self.db.insert_history(username, word)
        mean = self.db.find_word(word)
        if mean:
            c.send(mean[2].encode())
        else:
            c.send('单词未找到'.encode())

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
            self.find_all(c)
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

    def find_all(self, c):
        """
        处理查询请求
        :param c:
        :return:
        """
        while True:
            re = c.recv(1024).decode()
            data = re.split(' ')
            if data[0] == '##':
                return
            elif data[0] == 'Q':
                self.find_words(c, data[1], data[2])
            elif data[0] == 'H':
                self.find_history(c, data[1])

