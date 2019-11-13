#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-05 12:20:11
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 12:06:12
@Description: 
'''
import logging
from types import MethodType
LOG = logging.getLogger(__name__)


def to_str(kwstr):
    kwstr = kwstr
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
            if len(field_to_expand) == 0:
                fields[field] = val
                continue
            if field in field_to_expand:
                fields[field] = val
    LOG.debug(fields)
    return fields
