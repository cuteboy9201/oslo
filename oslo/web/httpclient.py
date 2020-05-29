#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Youshumin
@Date: 2019-11-05 12:05:59
@LastEditors  : YouShumin
@LastEditTime : 2020-01-13 06:24:26
@Description: 
"""
import json
import sys
import urllib

import tornado.web
from oslo.http.http_response import HttpResponse
from oslo.six import iteritems
from oslo.six.moves.urllib.parse import urlencode
from oslo.util import to_str
from tornado import gen, httpclient

py_version = sys.version_info.major


def encode_request_args(args):
    kw = []
    for item in args.items():
        if py_version == 2:
            quote_format = urllib.quote(to_str(item[1]))
        elif py_version == 3:
            quote_format = urllib.parse.quote(to_str(item[1]))
        kv = "=".join([item[0], quote_format])
        kw.append(kv)
    return "&".join(kw)


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
    def __init__(self, method, accept_format, protocol_type=None, port=80):
        self._method = method
        self._accept_format = accept_format
        self._port = port
        self._params = {}
        self._header = {}
        self._body_params = {}
        self._uri_pattern = None
        self._uri_params = None
        self._content = None

        self._request_connect_timeout = None
        self._request_read_timeout = None
        self._domain = None
        self._protocol_type = protocol_type

        if self._protocol_type is None:
            self._protocol_type = "http"

    def add_query_param(self, k, v):
        self._params[k] = v

    def add_body_params(self, k, v):
        self._body_params[k] = v

    def set_uri_pattern(self, pattern):
        self._uri_pattern = pattern

    def get_uri_pattern(self):
        return self._uri_pattern

    def set_uri_params(self, params):
        self._uri_params = params

    def set_method(self, method):
        self._method = method

    def set_accept_format(self, accept_format):
        self._accept_format = accept_format

    def set_query_params(self, params):
        self._params = params

    def set_body_params(self, body_params):
        self._body_params = body_params

    def get_body_params(self):
        return self._body_params

    def set_content(self, conent):
        self._content = conent

    def set_headers(self, headers):
        self._header = headers

    def add_header(self, k, v):
        self._header[k] = v

    def set_user_agent(self, agent):
        self.add_header("User-Agent", agent)

    def set_domain(self, domain):
        self._domain = domain

    def set_protocol_type(self, protocol_type):
        self._protocol_type = protocol_type

    # def get_request_url(self):
    #     return self._protocol_type + self._domain + self._uri_params

    def get_request_url_url(self):
        url = ""
        url += self._protocol_type
        url += self._domain
        url += self._uri_pattern
        if not url.endswith("?"):
            url += "?"
        url += urlencode(self._uri_params)
        if url.endswith("?"):
            url = url[0 : (len(url) - 1)]
        return url

    def fetch(self):
        if self._body_params:
            print(self._body_params)
            body = urlencode(self._body_params)
            print(body)
            self._content = body
        response = HttpResponse(
            host=self._domain,
            url=self._uri_pattern,
            method=self._method,
            headers=self._header,
            protocol=self._protocol_type,
            content=self._body_params,
            port=self._port,
            read_timeout=self._request_read_timeout,
            connect_timeout=self._request_connect_timeout,
        )
        # if self._body_params:
        #     body = urlencode(self._body_params)
        #     response.set_content(body, "utf-8", format="JSON")
        return response
