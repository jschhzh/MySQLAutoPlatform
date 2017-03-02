#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2017/3/2 上午10:39
@Author  : hz.c
@Site    : 
@File    : remote_backup.py
@Software: PyCharm
'''



from mysql.backup_recovery import DbBackup




if __name__ == '__main__':
    rem_conn_par = {"ip": "172.19.22.202", "user": "root", "password": "123456",}
    db_back_par = {"db_user":"root", "db_passwd": "123456", "db_port":"3306", "db_conf":"/etc/my.cnf","target_dir":"/data/backup/data/test",}
    phy_bak = DbBackup(db_back_par)
    result=phy_bak.remote_physic_backup(rem_conn_par)
    print result
    if result:
        print ('backup is ok!')
    else:
        print ('backup is faild!')
