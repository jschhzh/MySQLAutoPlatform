#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2017/2/13 下午3:12
@Author  : hz.c
@Site    : 
@File    : remote_cmd.py
@Software: PyCharm
'''

import subprocess
import paramiko
import os

class RunCommand(object):

    def __init__(self,user_info,env="{'USER': 'root', 'HOME': '/root'}"):
        self.user_info=user_info
        self.env=env

    # 返回命令正常输出
    def remote_cmd(self, cmd):
        if self.user_info["ip"] != "127.0.0.1":
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ip_addr = self.user_info["ip"]
            username = self.user_info["user"]
            passwd = self.user_info["password"]
            client.connect(
                ip_addr, port=int(22), username=username, password=passwd, timeout=5)
            stdin, stdout, stderr = client.exec_command(cmd)
            result = stdout.readlines()
            client.close()
            return result
        elif self.user_info["ip"] == "127.0.0.1":
            stdout = self.local_cmd(cmd, self.env)
            return stdout

    #返回命令错误输出
    def remote_cmd_err(self,cmd):
        if self.user_info["ip"] != "127.0.0.1":
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ip_addr = self.user_info["ip"]
            username = self.user_info["user"]
            passwd = self.user_info["password"]
            client.connect(
                ip_addr, port=int(22), username=username, password=passwd, timeout=5)
            stdin, stdout, stderr = client.exec_command(cmd)
            result = stderr.readlines()
            client.close()
            return result
        elif self.user_info["ip"] == "127.0.0.1":
            stdout = self.local_cmd(cmd, self.env)
            return stdout


    # loca_cmd函数为检查项需要执行操作系统命令的总入口
    def local_cmd(self, cmd, env):
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=env,
                             shell=True)
        stdout, stderr = p.communicate()
        return stdout


    def check_path(self,path):
        cmd='ls %s' % path
        print cmd
        result=self.remote_cmd_err(cmd)
        print result
        if result:
            cmd = 'mkdir -p %s' % path
            if self.user_info["ip"] != "127.0.0.1":
                result=self.remote_cmd_err(cmd)
                if not result:
                    return True
                False
            elif self.user_info["ip"] == "127.0.0.1":
                result = self.local_cmd(cmd)
                if not result:
                    return True
                False
        return True




