"""
数据库设置
"""
Database = 'mysql'
HOST = '*'
USERNAME = '*'
PASSWORD = '*'
ut_db = "create table if not exists user(id int primary key auto_increment,\
                            username varchar(16) unique not null, password varchar(32) not null );"
c_db = "create database if not exists EDICT charset utf8;"
u_db = "use EDICT"
ht_db = "create table if not exists history(id int primary key auto_increment,\
                                                username varchar(16) not null ,word varchar(32), time datetime);"
w_db = "create table if not exists word_list (id int primary key auto_increment,\
                                                word varchar(32) not null, ex text );"