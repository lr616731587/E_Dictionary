"""
服务端
"""
import getpass

from socket import *


class DictClient:
    def __init__(self, ip, port):
        self.ip = (ip, port)
        self.client = socket()
        self.client.connect(self.ip)

    def request(self):
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
                break
            else:
                print('请输入正确命令')

    def registered(self):
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
        i = 0
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

    def find_word(self):
        pass

    def second_view(self, user):
        while True:
            print("""
            ===================================user:{}==
            1.查单词            2.历史记录         3.注销
            ============================================
            """.format(user))
            data = input('CMD')
            if data == '1':
                self.find_word()
            elif data == '2':
                self.hitory()
            elif data == '3':
                return
            else:
                print('请输入正确命令')

    def hitory(self):
        pass

