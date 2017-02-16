#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2017/2/13 下午2:25
@Author  : hz.c
@Site    : 
@File    : backup.py
@Software: PyCharm
'''


import BaseModule.instance

class physic_backup(object):
    global pt_xtrabackup
    def __init__(self, db_user, db_passwd, db_port=None, conf='None', target_dir='None'):
        self.user = db_user
        self.passwd = db_passwd
        self.port = db_port
        if (conf == 'None'):
            self.default_file = '/etc/my.cnf'
        else:
            self.default_file = conf
        self.target_dir = target_dir

    # 备份
    def backup(self, user, passwd, port, defaults_file, target_dir):
        command = "{0} --defaults-file={1} --user={2} --password='{3}' --host=localhost --port={4} --no-timestamp --parallel=4 --throttle=500 --use-memory=2GB --stream=xbstream ./ > {5}".format(
            pt_xtrabackup, defaults_file, user, passwd, port, target_dir)

        return command
        '''
        status = self.local_cmd(command)
        if "completed OK!" in status:
            return True
        '''



class logical_backup(object):
    def __init__(self):
        pass
