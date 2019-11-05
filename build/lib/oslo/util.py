#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-05 12:20:11
@LastEditors: Youshumin
@LastEditTime: 2019-11-05 12:24:48
@Description: 
'''


def to_str(args):
    if not isinstance(args, basestring):
        args = str(args)
    if isinstance(args, unicode):
        args = args.encode("utf-8")
    return args
