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
from base_module import *

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
            try:
                command = "{0} --defaults-file={1} --user={2} --password='{3}' --host=localhost --port={4} --no-timestamp --parallel=4 --throttle=500 --use-memory=2GB --stream=xbstream ./ > {5}".format(
                    pt_xtrabackup, self.default_file, self.user, self.passwd, self.port, self.target_dir)
                print command
                reslut = remote_run_com.remote_cmd_err(command)
                last_line = reslut[-1]
                if 'completed OK!' in last_line:
                    return True
                else:
                    return False
            except Exception, BackupError:
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


class DbRecovery(object):
    """database recovery module"""

    # 启动文件、配置文件、数据文件路径、远程IP、账号、密码
    def __init__(self, source_url, db_conf):
        self.source_url = source_url
        self.db_conf = db_conf

    def remote_recovery(self, rem_conn_par):
        remote_run_com = RunCommand(rem_conn_par)
        db_control = MySQLControl(self.db_conf['mysqld_dir'], rem_conn_par)
        db_instance = MySQLOperations(db_conf['db_host'], db_conf['db_port'], db_conf['db_user'], db_conf['db_passwd'])


        if not db_instance.db_connect():
            pass
        else:
            db_instance.disconnect()
            result = db_control.stop_db()

            if not result:
                print "stop db is faild!"
                return False

        """ clear data dir"""
        cmd = "rm -rf %s*" % db_conf['data_dir']
        print cmd
        remote_run_com.remote_cmd(cmd)
        """Download the backup file"""
        # cmd = self.source_url + ' -C ' + self.db_conf['data_dir']
        # get_bak_file = remote_run_com.remote_cmd(cmd)
        get_bak_file = True
        if get_bak_file:
            cmd = "xbstream -x -v < %s%s -C  %s" % (
                self.db_conf['data_dir'], self.source_url.split('/')[-1], self.db_conf['data_dir'])
            print cmd
            copy_bak = remote_run_com.remote_cmd(cmd)
            if not copy_bak:
                try:
                    cmd = "%s --defalults_file=%s  --apply-log %s" % (
                        pt_xtrabackup, self.db_conf['cnf_dir'], self.db_conf[
                            'data_dir'])
                    print cmd
                    apply_log = remote_run_com.remote_cmd_err(cmd)
                    last_line = apply_log[-1]

                    if 'completed OK!' in last_line:
                        cmd = "chown -R mysql:mysql %s" % self.db_conf['data_dir']
                        chown_status = remote_run_com.remote_cmd(cmd)

                        result = db_control.start_db()
                        if result:
                            return True
                        return False
                    else:
                        return False
                except Exception, RecoveryError:
                    print RecoveryError
                    return RecoveryError


if __name__ == '__main__':
    rem_conn_par = {"ip": "172.19.22.202", "user": "root", "password": "123456",}
    db_conf = {"db_host": "172.19.22.202", "db_port": "3306", "db_user": "root", "db_passwd": "123456",
               "cnf_dir": "/etc/my.cnf",
               "mysqld_dir": "/etc/init.d/mysql",
               "data_dir": "/data/mysql/mysql3306/data/"}
    phy_bak = DbRecovery('/test_1', db_conf)
    result = phy_bak.remote_recovery(rem_conn_par)
    print result
