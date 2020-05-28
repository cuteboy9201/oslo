#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Youshumin
@Date: 2019-11-05 12:05:59
@LastEditors  : YouShumin
@LastEditTime : 2020-01-13 06:24:26
@Description: 
"""
import tornado.web
from tornado import httpclient
from oslo.util import to_str
import urllib
import json
from tornado import gen
import sys

py_version = sys.version_info.major


class AsyncRequest(object):
    """异步请求封装"""

    def __init__(self, url, method, body="", format="json", headers=None, **kwargs):
        self.url = url
        self.method = method.upper()
        self.body = body
        self.format = format
        self.req_data = kwargs
        self.headers = headers
        self._resp = None
        self._status = False
        self._client = httpclient.AsyncHTTPClient()
        self.CONNECT_TIMEOUT = 3
        self.REQUEST_TIMEOUT = 3
        super(AsyncRequest, self).__init__()

    def _encode_request_args(self, args):
        kw = []
        for item in args.items():
            if py_version == 2:
                quote_format = urllib.quote(to_str(item[1]))
            elif py_version == 3:
                quote_format = urllib.parse.quote(to_str(item[1]))
            kv = "=".join([item[0], quote_format])
            kw.append(kv)
        return "&".join(kw)

    def _encode_request_mothod(self):
        body = None
        url = self.url
        if self.method == "POST":
            if self.format != "json":
                body = self._encode_request_args(self.req_data)
            else:
                body = json.dumps(self.req_data)
        elif self.req_data:
            url += "?{}".format(self._encode_request_args(self.req_data))

        req_body = self.body or body
        return httpclient.HTTPRequest(
            url=url,
            method=self.method,
            body=req_body,
            headers=self.headers,
            connect_timeout=self.CONNECT_TIMEOUT,
            request_timeout=self.REQUEST_TIMEOUT,
        )

    @gen.coroutine
    def fetch(self):
        req = self._encode_request_mothod()
        try:
            self._resp = yield self._client.fetch(request=req, raise_error=False)
            self._resp = self._resp.body
            self._status = True
        except Exception as e:
            self._resp = {}
            raise gen.Return(self)

        if self.format == "json":
            try:
                self._resp = json.loads(self._resp)
            except Exception:
                self._resp = {}
        raise gen.Return(self)

    @property
    def data(self):
        return self._resp and self._resp["data"]

    @property
    def msg(self):
        return self._resp and self._resp["msg"]

    @property
    def resp(self):
        return self._resp


class Request(object):
    pass
