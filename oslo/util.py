#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-05 12:20:11
@LastEditors  : YouShumin
@LastEditTime : 2020-01-19 16:22:06
@Description: 
'''
import logging
import time
import datetime
from types import MethodType
import sys
LOG = logging.getLogger(__name__)

py_servion = sys.version_info.major


def to_str(kwstr):
    kwstr = kwstr
    if py_servion == 2:
        if not isinstance(kwstr, basestring):
            kwstr = str(kwstr)
        if isinstance(kwstr, unicode):
            kwstr = kwstr.encode("utf-8")
    return kwstr


def create_id():
    import uuid
    _id = uuid.uuid4()
    return "{}".format(_id)


def dbObjFormatToJson(self, field_to_expand=[]):
    fields = {}
    for field in [
            x for x in dir(self) if not x.startswith('_') and x != 'metadata'
    ]:
        val = self.__getattribute__(field)
        if not isinstance(val, MethodType):
            if isinstance(val, datetime.date):
                val = val.strftime("%Y-%m-%d %H:%M:%S")
            if len(field_to_expand) == 0:
                fields[field] = val
                continue
            if field in field_to_expand:
                fields[field] = val
    return fields
