#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2017/2/13 下午2:25
@Author  : hz.c
@Site    : 
@File    : backup_recovery.py
@Software: PyCharm
'''

pt_xtrabackup = "/usr/bin/innobackupex"

#备份模块
class DbBackup(object):
    global pt_xtrabackup
    def __init__(self, db_user, db_passwd, db_port=None, conf='None', target_dir='None'):
        self.user = db_user
        self.passwd = db_passwd
        self.port = int(db_port)
        if (conf == 'None'):
            self.default_file = '/etc/my.cnf'
        else:
            self.default_file = conf
        self.target_dir = target_dir

    # 物理备份
    def physic_backup(self):
        command = "{0} --defaults-file={1} --user={2} --password='{3}' --host=localhost --port={4} --no-timestamp --parallel=4 --throttle=500 --use-memory=2GB --stream=xbstream ./ > {5}".format(
            pt_xtrabackup, self.default_file, self.user, self.passwd, self.port, self.target_dir)

        return command

    # 逻辑备份
    def logical_backup(self):
        pass

