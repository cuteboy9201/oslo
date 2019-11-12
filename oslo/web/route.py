#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-12 12:30:28
@LastEditors: Youshumin
@LastEditTime: 2019-11-12 12:33:23
@Description:
'''

__all__ = ["route"]


class Route(object):

    def __init__(self):
        self.url_list = []

    def get_urls(self):
        return self.url_list

    def __call__(self, _url):
        def _(cls):
            self.url_list.append((_url, cls))
            return cls

        return _


route = Route()
del Route
