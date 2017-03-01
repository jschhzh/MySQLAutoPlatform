#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2017/2/24 下午1:59
@Author  : hz.c
@Site    : 
@File    : ftp.py
@Software: PyCharm
'''

from ftplib import FTP


class Ftp(object):
    def __init__(self, ftp_server, user, password, port=21, timeout=10):
        self.ftp_server = ftp_server
        self.user = user
        self.password = password
        self.port = int(port)
        self.timeout = int(timeout)

    def conn(self):
        self.ftp = FTP()
        try:
            self.ftp.connect(self.ftp_server, self.port, self.timeout)
            self.ftp.login(self.user,self.password)
        except Exception, Error:
            print Error
            return False
        return True

    def dis_conn(self):
        if (self.conn):
            self.conn.quit()
        self.conn = None

    def check_path(self):
        pass


    def upload_file(self):
        pass


    def down_load_file(self):
        pass
