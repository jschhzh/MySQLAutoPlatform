#!/usr/bin/python
# _*_ coding=utf-8 _*_

import MySQLdb


class instance(object):
    def __init__(self, host, port, user, passwd, dbname='None'):
        self.dbhost = host
        self.dbport = int(port)
        self.dbuser = user
        self.dbpassword = passwd
        if (dbname == 'None'):
            self.dbname = 'mysql'
        else:
            self.dbname = dbname

    def connect(self):
        try:
            self.conn = MySQLdb.connect(host="%s", port="%s", user="%s", passwd="%s", db="%s") % (
            self.dbhost, self.dbport, self.dbuser, self.dbpassword, self.dbname)
        except Exception, error:
            print error
            return False
        return True

    def disconnect(self):
        if (self.conn):
            self.conn.close()
        self.conn = None

    def execsql(self, sql):
        cursor = self.conn.cursor(cursorclass=cursors.DictCursor)
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def fetchone(self,sql):
        cursor = self.conn.cursor(cursorclass=cursors.DictCursor)
        cursor.execute(sql)
        onedata = cursor.fetchone()
        cursor.close()
        return onedata

    def fetchall(self,sql):
        cursor = self.conn.cursor(cursorclass=cursors.DictCursor)
        cursor.execute(sql)
        alldata = cursor.fetchall()
        cursor.close()
        return alldata

