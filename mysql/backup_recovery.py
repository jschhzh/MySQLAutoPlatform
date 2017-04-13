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

        if db_instance.db_connect():
            db_instance.disconnect()
            result = db_control.stop_db()
            if not result:
                print "stop db is faild!"
                return False
        else:
            pass

        """ clear data dir"""
        cmd = "rm -rf %s*" % db_conf['data_dir']
        print cmd
        remote_run_com.remote_cmd(cmd)
        """Download the backup file"""
        cmd = self.source_url + ' -P ' + self.db_conf['data_dir']
        print cmd
        get_bak_file = remote_run_com.remote_cmd(cmd)
        #get_bak_file = True
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

    def remote_recovery_anytime(self,rem_conn_par,binlog_info,recovery_par):
        remote_run_com = RunCommand(rem_conn_par)
        if self.remote_recovery(rem_conn_par):
            cmd = "cat %sxtrabackup_binlog_info" % db_conf['data_dir']
            result = remote_run_com.remote_cmd(cmd, 'all')
            start_binlog_file = result.split()[0]
            start_binlog_pos = result.split()[1]
            stop_binlog_file=recovery_par['stop_binlog_file']
            stop_binlog_time=recovery_par['stop_binlog_time']
            for binlog_file in binlog_info:
                cmd = self.binlog_file['source_url'] + ' -P ' + self.db_conf['data_dir']
                get_binlog_file = remote_run_com.remote_cmd(cmd)

    def replication_recovery(self, rem_conn_par, rep_info):
        remote_run_com = RunCommand(rem_conn_par)
        db_instance = MySQLOperations(db_conf['db_host'], db_conf['db_port'], db_conf['db_user'], db_conf['db_passwd'])
        if self.remote_recovery(rem_conn_par):
            cmd = "cat %sxtrabackup_binlog_info" % db_conf['data_dir']
            result = remote_run_com.remote_cmd(cmd, 'all')
            gtid = ''.join(result.split()[2:])
            db_instance.db_connect()
            sql = "reset master;set SET GLOBAL gtid_purged=\'%s\'" % gtid
            print sql
            db_instance.exec_sql(sql)
            sql = "CHANGE MASTER TO master_host=\'%s\',master_port=\s,master_user=\'%s\', master_password=\'%s\',master_connect_retry=10,MASTER_AUTO_POSITION = 1;" % (
                rep_info['master_host'], int(rep_info['master_port']), rep_info['rep_user'], rep_info['rep_passwd'])
            db_instance.exec_sql(sql)
            sql = "start slave;select sleep(3);show slave status;"
            result = db_instance.fetch_all(sql)
            print result
        else:
            print 'backup recovery faild!'


if __name__ == '__main__':
    rem_conn_par = {"ip": "", "user": "root", "password": "",}
    db_conf = {"db_host": "", "db_port": "3302", "db_user": "", "db_passwd": "",
               "cnf_dir": "/etc/my3302.cnf",
               "mysqld_dir": "/etc/init.d/mysql3302",
               "data_dir": "/data2/mysql/data/"}
    phy_bak = DbRecovery("wget --ftp-user=", db_conf)
    result = phy_bak.remote_recovery(rem_conn_par)
    #result = phy_bak.replication_recovery(rem_conn_par)
    print result
