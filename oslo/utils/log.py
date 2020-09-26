#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: YouShumin
Date: 2020-09-08 16:45:57
LastEditTime: 2020-09-26 15:37:56
LastEditors: YouShumin
Description: Another flat day
FilePath: /oslo/oslo/utils/log.py
'''
import os
import fcntl
from tornado.options import define, options
from oslo.utils.parameter_helper import get_today_date
import json 
import traceback
import time 
import logging 

LOG = logging.getLogger(__name__)
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


def make_daily_path(msg):
    # 日志文件名
    msg_type = msg["mold"]
    return "{}_{}.txt".format(msg_type.lower(), get_today_date())

def write_json_msg(dir, msg):
    path = make_daily_path(msg)
    abs_path = os.path.join(dir, path)
    abs_dir = os.path.split(abs_path)[0]

    if not os.path.isdir(abs_dir):
        os.makedirs(abs_dir)

    try:
        f = open(abs_path, "a")
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write("{}\n".format(json.dumps(msg)))
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        f.close()
    except Exception as e:
        LOG.error(traceback.format_exc())
        time.sleep(0.0001)