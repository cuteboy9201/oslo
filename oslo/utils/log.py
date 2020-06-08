import os

from tornado.options import define, options


class LogHandler(object):
    def __init__(self, LOGFILE):
        dir_name = os.path.dirname(LOGFILE)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        options.log_file_prefix = LOGFILE
        options.log_rotate_mode = "time"
        options.log_rotate_when = "D"
        options.log_rotate_interval = 1
        options.log_file_num_backups = 60
        options.log_to_stderr = False
        super(LogHandler, self).__init__()
