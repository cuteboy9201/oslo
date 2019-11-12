#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-10-31 22:58:44
@LastEditors: Youshumin
@LastEditTime: 2019-11-12 12:43:20
@Description:
'''

import json
import tornado
from tornado.escape import json_decode
from tornado.util import ObjectDict


class MixinRequestHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(MixinRequestHandler, self).__init__(
            application, request, **kwargs)
        self.headers = self.request.headers

    def write(self, data, jsond=""):
        if jsond:
            self.set_header("Context-Type", "text/json;charset=utf-8")
            self.set_header("Content-Type", "application/json;charset=UTF-8")
            self.set_header("Cache-Control", "no-cache")
        super(MixinRequestHandler, self).write(data)

    def send_error(self, msg=None, callback=None, code=500):
        send_json = dict(statusCode=code, msg=msg or "", data="")
        send_json_format = json.dumps(send_json, ensure_ascii=True)
        if callable:
            send_json_format = "{}({})".format(callback, send_json_format)
        self.write(send_json_format, True)
        self.finish()

    def send_ok(self, data=None, callback=None, code=200):
        send_json = dict(statusCode=code, msg="", data=data)
        send_json_format = json.dumps(send_json, ensure_ascii=True)
        if callback:
            send_json_format = "{}({})".format(callback, send_json_format)
        self.write(send_json_format)
        self.finish()

    def get_client_ip(self):
        xff = self.headers.get("X-Forwarded-For", "")
        if xff:
            return xff.split(",")[0]
        return self.headers.get("X-Real-Ip", "") or self.request.remote_ip

    def request_body(self):
        data = dict()
        _req_body = self.request.body

        if _req_body:
            try:
                return ObjectDict(json_decode(_req_body))
            except Exception:
                pass

        for k in self.request.arguments:
            v = self.get_argument(k)
            data[k] = v[0] if len(v) == 1 else v
        return

    def get_args(self, key, default="", data_type=None):
        data_type = data_type or unicode
        try:
            data = self.get_argument(key)
            if callable(data_type):
                return data_type(data)
            return data
        except (tornado.web.MissingArgumentError, ValueError):
            return default
