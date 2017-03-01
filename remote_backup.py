#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2017/2/21 上午10:31
@Author  : hz.c
@Site    : 
@File    : remote_backup.py
@Software: PyCharm
'''

from mysql.backup_recovery import DbBackup
from public.remote_cmd import RunCommand
from public.ftp import Ftp


# 远程物理备份
def remote_physic_backup(rem_conn_par, db_back_par):
    # DbUser,DbPasswd,3306,conf,target_dir
    phy_bak = DbBackup(db_back_par['dbuser'], db_back_par['dbpasswd'], db_back_par['dbport'], db_back_par['dbconf'],
                       db_back_par['targetdir'])
    cmd = phy_bak.physic_backup()
    RemoteRunCom = RunCommand(rem_conn_par)
    bakup_path='/'.join(db_back_par['targetdir'].split('/')[:-1])
    checkpath=RemoteRunCom.check_path(bakup_path)
    if checkpath:
        reslut = RemoteRunCom.remote_cmd_err(cmd)
        last_line = reslut[-1]
        if 'completed OK!' in last_line:
            return True
        else:
            False
    else:
        print 'check remote path!'
        return False


if __name__ == '__main__':
    rem_conn_par = {"ip": "172.19.22.202", "user": "root", "password": "123456"}
    db_back_par = {"dbuser": "root", "dbpasswd": "123456", "dbport": "3306", "dbconf": "/etc/my.cnf",
                   "targetdir": "/data/backup/data/test"}
    result=remote_physic_backup(rem_conn_par, db_back_par)
    print result
    if result:
        print 'backup is ok!'
    else:
        print 'backup is faild!'




