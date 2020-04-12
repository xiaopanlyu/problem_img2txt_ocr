'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: start and config snipaste
@Author: Allen
@Date: 2020-04-01 18:34:43
@LastEditTime: 2020-04-05 22:29:20
@LastEditors: Allen
'''
from subprocess import Popen, PIPE
import time
import os
import subprocess


class snipaste(object):
    def __init__(self):
        self.proc = None
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.root_path = os.path.join(self.cur_path, 'Snipaste-1.16.2-x64')
        self.exec_path = os.path.join(self.root_path, 'Snipaste.exe')

    def set_quick_save_path(self, config_path, monitor_path):
        result = list()
        with open('%s' % (config_path), 'r+', encoding='utf-8') as f:
            for line in f.readlines():
                if 'auto_save_dir' in line:
                    line = ''.join(['auto_save_dir', '=', monitor_path, '\n'])
                if 'quick_save_dir' in line:
                    line = ''.join(['quick_save_dir', '=', monitor_path, '\n'])
                result.append(line)
            f.seek(0)
            f.truncate()
            f.write("{}\n".format(''.join(result)))
            f.close()

    def stop_snipaste(self):
        if self.proc:
            self.proc.kill()  # 终止子进程
            self.proc.communicate()
            self.proc.terminate()
            print('test')
        # stop_cmd = 'snip --exit'
        # ret = subprocess.call([exec_path, stop_cmd],
        #                       shell=True,
        #                       stdout=subprocess.PIPE,
        #                       stderr=subprocess.PIPE,
        #                       encoding="utf-8",
        #                       timeout=1)

    def start_snipaste(self, monitor_path):
        config_path = os.path.join(self.root_path, 'config.ini')
        self.set_quick_save_path(config_path, monitor_path)
        config_param = '--config=%s' % config_path
        # print(config_param)
        # quick_save_param = 'snip -o quick-save'
        # subprocess.run([exec_path, config_param])

        # cmd_line = " ".join([exec_path, config_param])
        # os.system(cmd_line)

        if not self.proc:
            self.proc = subprocess.Popen(
                [self.exec_path, config_param],
                shell=True,
            )


snip = snipaste()
