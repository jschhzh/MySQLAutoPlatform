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
class run_command(object):

    def __init__(self,user_info,env="{'USER': 'root', 'HOME': '/root'}"):
        self.user_info=user_info
        self.env=env

    # remote_cmd函数为检查项需要执行操作系统命令的总入口
    def remote_cmd(self, user_info, cmd, env):
        if user_info["ip"] != "127.0.0.1":
            import paramiko
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ip_addr = user_info["ip"]
            username = user_info["user"]
            passwd = user_info["password"]
            client.connect(
                ip_addr, port=int(22), username=username, password=passwd, timeout=5)
            stdin, stdout, stderr = client.exec_command(cmd)
            result = stdout.read()
            client.close()
            return result
        elif user_info["ip"] == "127.0.0.1":
            stdout = self.loca_cmd(cmd, env)
            return stdout


    # loca_cmd函数为检查项需要执行操作系统命令的总入口
    def loca_cmd(self, cmd, env):
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=env,
                             shell=True)
        stdout, stderr = p.communicate()
        return stdout