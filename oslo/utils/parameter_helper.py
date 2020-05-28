#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: YouShumin
@Date: 2020-05-18 14:38:20
@LastEditTime: 2020-05-18 14:38:21
@LastEditors: YouShumin
@Description: 
@FilePath: /oslo/oslo/utils/parameter_helper.py
"""

import base64
import hashlib
import socket
import sys
import time
import uuid

from oslo.utils.compat import ensure_bytes, ensure_string

TIME_ZONE = "GMT"
FORMAT_ISO_8601 = "%Y-%m-%dT%H:%M:%SZ"
FORMAT_RFC_2616 = "%a, %d %b %Y %H:%M:%S GMT"
FORMAT_TODAY_DATE = "%Y%m%d"


def get_uuid():
    name = socket.gethostname() + str(uuid.uuid1())
    namespace = uuid.NAMESPACE_URL
    return str(uuid.uuid5(namespace, name))


def get_iso_9061_date():
    return time.strftime(FORMAT_ISO_8601, time.gmtime())


def get_rfc_2616_date():
    return time.strftime(FORMAT_RFC_2616, time.gmtime())


def get_today_date():
    return time.strftime(FORMAT_TODAY_DATE, time.gmtime())


def md5_sum(content):
    content_bytes = ensure_bytes(content)
    md5_bytes = hashlib.md5(content_bytes).digest()
    return ensure_string(base64.standard_b64encode(md5_bytes))


if __name__ == "__main__":
    print(get_today_date())
