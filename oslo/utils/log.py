#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: YouShumin
Date: 2020-09-08 16:45:57
LastEditTime: 2020-09-26 15:30:42
LastEditors: YouShumin
Description: Another flat day
FilePath: /oslo/oslo/utils/log.py
'''
import os

from tornado.options import define, options

class LogHandler(object):
    def __init__(self, logfile, num, stder=False):
        dir_name = os.path.dirname(logfile)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        options.log_file_prefix = logfile
        options.log_rotate_mode = "time"
        options.log_rotate_when = "D"
        options.log_rotate_interval = 1
        options.log_file_num_backups = num
        options.log_to_stderr = stder
        super(LogHandler, self).__init__()
