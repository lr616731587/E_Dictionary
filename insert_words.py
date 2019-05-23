import pymysql
import re

from e_dictionary.settings import *


class InsertWord:
    """
    单词表
    """
    def __init__(self):
        self.db = pymysql.connect(
            HOST,
            USERNAME,
            PASSWORD,
            Database,
            charset='utf8'
        )
        self.cur = self.db.cursor()
        self.cur.execute(c_db)  # 创建数据库
        self.cur.execute(u_db)  # 进入数据库
        self.cur.execute(w_db)  # 创建user表

    def insert_word(self):
        """
        将单词插入数据库
        :return:
        """
        sql = 'insert into word_list (word, ex) VALUES (%s, %s);'
        with open('dict.txt', 'r') as f:
            for line in f:
                # 　获取匹配内容元组　(word,mean)
                tup = re.findall(r'(\w+)\s+(.*)', line)[0]

                try:
                    self.cur.execute(sql, tup)
                    self.db.commit()
                except Exception as e:
                    self.db.rollback()
                    print(e)

