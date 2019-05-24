"""
客户端
"""
import getpass

from socket import *


class DictClient:
    def __init__(self, ip, port):
        self.ip = (ip, port)
        self.client = socket()
        self.client.connect(self.ip)

    def request(self):
        """
        一级主界面
        :return:
        """
        while True:
            print("""
            ============================================
            1.注册            2.登录               3.退出
            ============================================
            """)
            data = input('CMD')
            if data == '1':
                self.registered()
            elif data == '2':
                self.login()

            elif data == '3':
                self.client.send(b'E')
                print('谢谢使用')
                return
            else:
                print('请输入正确命令')

    def registered(self):
        """
        注册账号请求
        :return:
        """
        while True:
            username = input('用户名:')
            password = getpass.getpass()
            tell = input('手机号:')
            if (' ' in username) or (' ' in password):
                print('用户名中包含非法字符')
                continue

            msg = 'R {} {} {}'.format(username, password, tell)
            self.client.send(msg.encode())
            data = self.client.recv(1024).decode()
            if data == 'ok':
                print('注册成功')
                self.second_view(username)
                return
            else:
                print('{}'.format(data))
                return

    def login(self):
        """
        登录请求
        :return:
        """
        i = 0  # 密码错误计数
        while True:
            username = input('User:')
            password = getpass.getpass()
            msg = 'L {} {}'.format(username, password)
            self.client.send(msg.encode())
            data = self.client.recv(1024).decode()
            if data == 'ok':
                print('登录成功')
                self.second_view(username)
                return
            else:
                if data == '账号或密码错误':
                    print(data)
                    i += 1
                    if i > 2:
                        re = input('是否重置密码（Y/N）')
                        if re == 'Y':
                            self.reset()
                            self.second_view(username)
                            return
                        else:
                            break
                else:
                    print(data)

    def reset(self):
        """
        发送重置密码请求
        :return:
        """
        username = input('请输入需要重置的账号')
        tell = input('请输入绑定的手机号')
        msg = 'C {} {}'.format(username, tell)
        self.client.send(msg.encode())
        data = self.client.recv(1024).decode()
        if data == 'ok':
            password = getpass.getpass()
            self.client.send(password.encode())
            req = self.client.recv(1024).decode()
            print(req)
            return
        else:
            print(data)
            self.request()

    def find_word(self, username):
        """
        发送查询单词请求
        :param username:
        :return:
        """
        while True:
            word = input('请输入要查找的单词')
            if word == '##':
                print("退出查询")
                break
            msg = 'Q {} {}'.format(word, username)
            self.client.send(msg.encode())
            data = self.client.recv(2048).decode()
            print(word, ':', data)

    def second_view(self, user):
        """
        二级界面
        :param user:
        :return:
        """
        while True:
            print("""
            ===================================user:{}==
            1.查单词          2.历史记录          3.注销
            ============================================
            """.format(user))
            data = input('CMD')
            if data == '1':
                self.find_word(user)
            elif data == '2':
                self.history(user)
            elif data == '3':
                return
            else:
                print('请输入正确命令')

    def history(self, username):
        """
        发送查看历史记录请求
        :param username:
        :return:
        """
        msg = 'H {}'.format(username)
        self.client.send(msg.encode())
        while True:
            data = self.client.recv(1024).decode()
            if data == '##':
                break
            print(data)


