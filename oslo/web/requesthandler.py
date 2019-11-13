#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-10-31 22:58:44
@LastEditors: Youshumin
@LastEditTime: 2019-11-13 11:59:16
@Description:
'''

import json
import tornado
from tornado.escape import json_decode
from tornado.util import ObjectDict
from tornado.options import define, options


class MixinRequestHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(MixinRequestHandler, self).__init__(
            application, request, **kwargs)
        self.headers = self.request.headers

    def write_client(self, data, jsond=""):
        if jsond:
            self.set_header("Context-Type", "text/json;charset=utf-8")
            self.set_header("Content-Type", "application/json;charset=UTF-8")
            self.set_header("Cache-Control", "no-cache")
        if options.debug:
            self.set_header("Access-Control-Allow-Origin",
                            "{}".format(self.headers.get("Origin", "")))
        elif options.allow_host:
            if self.headers.get("Origin", "") in options.allow_host:
                self.set_header("Access-Control-Allow-Origin",
                                "{}".format(self.headers.get("Origin", "")))

        self.write(data)

    def send_error(self, msg=None, callback=None, code=500):
        send_json = dict(statusCode=code, msg=msg or "", data="")
        send_json_format = json.dumps(send_json, ensure_ascii=True)
        # if callable:
        #     send_json_format = "{}({})".format(callback, send_json_format)
        self.write_client(send_json_format, True)
        self.finish()

    def send_fail_json(self, msg=None, callback=None, code=500):
        return self.send_error(msg=msg, code=code)

    def send_ok(self, data=None, callback=None, code=200):
        send_json = dict(statusCode=code, msg="", data=data)
        send_json_format = json.dumps(send_json, ensure_ascii=True)
        # if callback:
        #     send_json_format = "{}({})".format(callback, send_json_format)
        self.write_client(send_json_format)
        self.finish()

    def send_ok_json(self, data=None, callback=None, code=200):
        return self.send_ok(data=data, code=code)

    def get_client_ip(self):
        xff = self.headers.get("X-Forwarded-For", "")
        if xff:
            return xff.split(",")[0]
        return self.headers.get("X-Real-Ip", "") or self.request.remote_ip

    def from_data(self):
        return self.request_body()

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
        return data

    def get_args(self, key, default="", data_type=None):
        data_type = data_type or unicode
        try:
            data = self.get_argument(key)
            if callable(data_type):
                return data_type(data)
            return data
        except (tornado.web.MissingArgumentError, ValueError):
            return default

    def options(self, *args, **kwargs):
        """
        处理测试时候的跨域问题
        """
        self.set_header("Access-Control-Allow-Methods",
                        "GET,PUT,POST,PATCH,DELETE,HEAD,OPTIONS")

        self.set_header("Connection", "keep-alive")
        if options.debug:
            self.set_header(
                "Access-Control-Allow-Origin",
                "{}".format(self.request.headers.get("Origin", "")))

            self.set_header(
                "Access-Control-Allow-Headers", "{}".format(
                    self.request.headers.get("Access-Control-Request-Headers",
                                             "")))
        elif options.allow_host:
            if self.headers.get("Origin", "") in options.allow_host:
                self.set_header("Access-Control-Allow-Origin",
                                "{}".format(self.headers.get("Origin", "")))
                self.set_header(
                    "Access-Control-Allow-Headers", "{}".format(
                        self.request.headers.get("Access-Control-Request-Headers",
                                                 "")))
        self.write("")
        self.set_status(204)
        self.finish()
