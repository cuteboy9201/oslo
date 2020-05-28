#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: YouShumin
@Date: 2020-05-18 14:53:43
@LastEditTime: 2020-05-18 14:53:43
@LastEditors: YouShumin
@Description: 
@FilePath: /oslo/oslo/utils/compat.py
"""

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)

if PY2:
    from base64 import encodestring as b64_encode_bytes
    from base64 import decodestring as b64_decode_bytes

    def ensure_bytes(s, encodeing="utf-8", errors="strict"):
        if isinstance(s, unicode):
            return s.encode(encodeing, errors)
        if isinstance(s, str):
            return s
        raise ValueError("Expected str or unicode, received %s." % type(s))

    def ensure_string(s, encodeing="utf-8", errors="strict"):
        if isinstance(s, unicode):
            return s.encode(encodeing, errors)
        if isinstance(s, str):
            return s
        raise ValueError("Expected str or unicode, received %s." % type(s))


else:
    from base64 import encodebytes as b64_encode_bytes
    from base64 import decodebytes as b64_decode_bytes

    def ensure_bytes(s, encoding="utf-8", errors="strict"):
        if isinstance(s, str):
            return bytes(s, encoding=encoding)
        if isinstance(s, bytes):
            return s
        if isinstance(s, bytearray):
            return bytes(s)
        raise ValueError("Expected str or bytes or bytearray, received %s." % type(s))

    def ensure_string(s, encoding="utf-8", errors="strict"):
        if isinstance(s, str):
            return s
        if isinstance(s, (bytes, bytearray)):
            return str(s, encoding="utf-8")
        raise ValueError("Expected str or bytes or bytearray, received %s." % type(s))
