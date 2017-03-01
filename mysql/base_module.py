#!/usr/bin/python
# _*_ coding=utf-8 _*_

import pymysql


class MySQLOperations(object):
    def __init__(self, db_host, db_port, db_user, db_passwd, db_name='mysql', charset='utf8'):
        self.conn_conf = {'host': db_host, 'port': db_port, 'user': db_user, 'password': db_passwd, 'db': db_name,
                          'charset': charset, 'cursorclass': pymysql.cursors.DictCursor,
                          }

    #创建数据库连接
    def db_connect(self):
        try:
            self.connection = pymysql.connect(**self.conn_conf)
            return True
        except Exception, ConnectionError:
            print (ConnectionError)
            return ConnectionError

    #关闭数据库连接
    def disconnect(self):
        if (self.connection):
            self.connection.close()
        else:
            self.connection = None

    #执行sql命令
    def exec_sql(self, sql):
        self.cursor = self.connection.cursor()
        exec_sql = self.cursor.execute(sql)
        self.connection.commit()
        return exec_sql

    #获取一条数据
    def fetch_one(self, sql):
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    #获取全部数据
    def fetch_all(self, sql):
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


