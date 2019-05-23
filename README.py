"""
1. 确定技术

   通信    tcp通信
   并发    多进程并发
   数据库  mysql

2. 确定数据库 ：

   * 建表

     用户表 ： id   name   passwd   tell


     历史记录：id   name   word   time


     单词表： id   word  mean


   * 将单词本存入到数据库

3. 结构设计

   客户端
   服务端 （处理数据）

4. 功能分析

   客户端和服务端分别需要实现哪些功能

   网络模型

   注册

      客户端  * 输入注册信息
              * 将信息发送给服务端
	      * 等待反馈

      服务端  * 接收注册信息
              * 验证用户是否存在
	      * 插入数据库
              * 将信息反馈个客户端

   登录
      客户端 * 输入登录信息
             * 发送请求
	     * 得到回复

      服务端 * 接收请求
             * 判断是否允许登录
	     * 反馈结果

   查单词
   历史记录


协议指定 ：  注册  R name passwd
             登录  L name  passwd
             重置  C name  tell




"""

