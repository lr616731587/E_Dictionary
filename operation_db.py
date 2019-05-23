import pymysql
import hashlib
import warnings

from e_dictionary.settings import *


warnings.filterwarnings('ignore')


class DataBase:
    """
    电子辞典数据库操作
    """
    def __init__(self):
        self.db = pymysql.connect(
            HOST,
            USERNAME,
            PASSWORD,
            Database,
            charset='utf8'
        )

    def create_cursor(self):
        """
        创建游标
        :return:
        """
        self.cur = self.db.cursor()
        self.cur.execute(c_db)  # 创建数据库
        self.cur.execute(u_db)  # 进入数据库
        self.cur.execute(ut_db)  # 创建user表
        self.cur.execute(ht_db)  # 创建history表

    def registered(self, username, password, tell):
        """
        注册
        :param username:
        :param password:
        :param tell:
        :return:
        """
        tell = self.md5(username, tell)
        password = self.md5(username, password)
        sql = "select * from user where username='%s';" % username
        self.cur.execute(sql)
        if self.cur.fetchone():
            return False
        sql = "insert into user(username, password, tell) values (%s, %s, %s);"
        try:
            self.cur.execute(sql, [username, password, tell])
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False
        return True

    def login(self, username, password):
        """
        登录验证
        :param username:
        :param password:
        :return:
        """
        password = self.md5(username, password)
        sql = "select * from user where username='%s';" % username
        self.cur.execute(sql)
        lo = self.cur.fetchone()
        if lo:
            sql = "select * from user where username='%s' and password='%s';" % (username, password)
            self.cur.execute(sql)
            re = self.cur.fetchone()
            if re:
                return 'ok'
            return '账号或密码错误'
        return '账号不存在'

    def close(self):
        """
        关闭
        :return:
        """
        self.cur.close()
        self.db.close()

    def md5(self, username, data):
        """
        MD5加密
        :param password:
        :return:
        """
        md5 = hashlib.md5((username + '!@#$').encode())
        md5.update(data.encode())
        return md5.hexdigest()

    def rest(self, username, tell):
        """
        重置验证
        :param username:
        :param tell:
        :return:
        """
        sql = "select * from user where username='%s' and tell='%s'" % (username, self.md5(username, tell))
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    def updata(self, username, tell, psd):
        """
        重置密码
        :param username:
        :param tell:
        :param psd:
        :return:
        """
        sql = "update user set password='%s' where username='%s' and tell='%s';" % (self.md5(username, psd), username, self.md5(username, tell))
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
            return False
        return True


