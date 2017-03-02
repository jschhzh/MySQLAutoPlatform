#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2017/2/13 下午2:25
@Author  : hz.c
@Site    : 
@File    : backup_recovery.py
@Software: PyCharm
'''
from MySQLAutoPlatform.public.remote_cmd import RunCommand
from base_module import MySQLOperations

pt_xtrabackup = "/usr/bin/innobackupex"


class DbBackup(object):
    """database backup module,"""
    global pt_xtrabackup

    def __init__(self, db_back_par):
        self.user = db_back_par['db_user']
        self.passwd = db_back_par['db_passwd']
        self.port = int(db_back_par['db_port'])
        if (db_back_par['db_conf'] == 'None'):
            self.default_file = '/etc/my.cnf'
        else:
            self.default_file = db_back_par['db_conf']
        self.target_dir = db_back_par['target_dir']

    # 物理备份
    def physic_backup(self):
        command = "{0} --defaults-file={1} --user={2} --password='{3}' --host=localhost --port={4} --no-timestamp --parallel=4 --throttle=500 --use-memory=2GB --stream=xbstream ./ > {5}".format(
            pt_xtrabackup, self.default_file, self.user, self.passwd, self.port, self.target_dir)
        return command

    # 远程物理备份
    def remote_physic_backup(self, rem_conn_par):
        remote_run_com = RunCommand(rem_conn_par)
        bakup_path = '/'.join(self.target_dir.split('/')[:-1])
        check_path = remote_run_com.check_path(bakup_path)
        if check_path:
            command = "{0} --defaults-file={1} --user={2} --password='{3}' --host=localhost --port={4} --no-timestamp --parallel=4 --throttle=500 --use-memory=2GB --stream=xbstream ./ > {5}".format(
                pt_xtrabackup, self.default_file, self.user, self.passwd, self.port, self.target_dir)
            print command
            reslut = remote_run_com.remote_cmd_err(command)
            last_line = reslut[-1]
            try:
                if 'completed OK!' in last_line:
                    return True
                else:
                    return False
            except Exception,BackupError:
                print BackupError
                return BackupError
        else:
            print ('check remote path!')
            return False

    # 逻辑备份
    def logical_backup(self):
        pass


# 日志备份模块
class BinlogBackup(object):
    def __init__(self):
        pass

    def remote_backup_log(self):
        command = ''


# 恢复模块
class DbRecovery(object):
    #启动文件、配置文件、数据文件路径、远程IP、账号、密码
    def __init__(self):
        pass

    def remote_recovery(self):
        pass
