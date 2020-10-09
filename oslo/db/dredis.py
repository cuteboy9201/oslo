#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: YouShumin
Date: 2020-09-26 16:02:37
LastEditTime: 2020-10-09 10:37:46
LastEditors: YouShumin
Description: Another flat day
FilePath: /oslo/oslo/db/dredis.py
'''
import platform
import socket
import warnings

import redis
from redis import connection

if platform.system() == "Darwin":
    OSTYPE = "mac"
elif platform.system() == "Linux":
    OSTYPE = "linux"
else:
    OSTYPE = "linux"
_rv = redis.__version__.split(".")

# assert _rv[0] >= "2" and _rv[1].rjust(2, "0") >= "10"

TCP_CLOSE_WAIT = 8 



class NewConnection(redis.Connection):

    def disconnect(self):

        self._parser.on_disconnect()
        
        if self._sock is None:
            return 
        
        
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except(OSError, socket.error):
            pass 
        try:
            self._sock.close()
        except socket.error:
            pass     
        self._sock = None 
    
    def validate(self):
        if self._sock is None:
            return 
        try:
            if OSTYPE == "mac":
                state = ord(
                    self._sock.getsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL,
                                          1))
            else:
                state = ord(
                    self._sock.getsockopt(socket.SOL_TCP, socket.TCP_INFO, 1))
            if state == TCP_CLOSE_WAIT:
                raise redis.ConnectionError()
        except socket.error:
            raise redis.ConnectionError()
        return True 

class NewRedisPool(redis.ConnectionPool):

    def __init__(self, connection_class=NewConnection, max_connections=None, **connection_kwargs):
        super(NewRedisPool, self).__init__(connection_class=connection_class, max_connections=max_connections, **connection_kwargs) 
    
    def get_connection(self, command_name, *keys, **options):
        self._checkpid()
        connection = None 
        while 1:
            try:
                connection = self._available_connections.pop(0)
                connection.validate()
                break 
            except IndexError:
                connection = self.make_connection()
                break 
            except redis.ConnectionError:
                if connection is not None:
                    connection.disconnect()
        self._in_use_connections.add(connection)
        return connection

    def release(self, connection):
        self._checkpid()
        if connection.pid != self.pid:
            return
        self._in_use_connections.remove(connection)
        if self._available_connections:
            connection.disconnect()
            return
        self._available_connections.append(connection)

class RedisConn(redis.StrictRedis):
    def __init__(self,
                 host="localhost",
                 port=6379,
                 db=0,
                 password=None,
                 socket_timeout=None,
                 socket_connect_timeout=1,
                 socket_keepalive=None,
                 socket_keepalive_options=None,
                 connection_pool=None,
                 unix_socket_path=None,
                 encoding='utf-8',
                 encoding_errors='strict',
                 charset=None,
                 errors=None,
                 decode_responses=False,
                 retry_on_timeout=False,
                 ssl=False,
                 ssl_keyfile=None,
                 ssl_certfile=None,
                 ssl_cert_reqs=None,
                 ssl_ca_certs=None):
        if not connection_pool:
            if charset is not None:
                warnings.warn(
                    DeprecationWarning(
                        '"Charset" is deprecated. Use "encoding" instead'))
                encoding = charset
            if errors is not None:
                warnings.warn(
                    DeprecationWarning(
                        '"errors" is deprecated. Use "encoding_error" instead')
                )
                encoding_errors = errors

            kwargs = {
                'db': db,
                'password': password,
                'socket_timeout': socket_timeout,
                'encoding': encoding,
                'encoding_errors': encoding_errors,
                'decode_responses': decode_responses,
                'retry_on_timeout': retry_on_timeout
            }

            if unix_socket_path is not None:
                kwargs.update({
                    'path':
                    unix_socket_path,
                    'connection_class':
                    redis.UnixDomainSocketConnection
                })
            else:
                kwargs.update({
                    'host':
                    host,
                    'port':
                    port,
                    'socket_connect_timeout':
                    socket_connect_timeout,
                    'socket_keepalive':
                    socket_keepalive,
                    'socket_keeplive_options':
                    socket_keepalive_options
                })
                if ssl:
                    kwargs.update({
                        'connection_class': redis.SSLConnection,
                        'ssl_keyfile': ssl_keyfile,
                        'ssl_certfile': ssl_cert_reqs,
                        'ssl_ca_caerts': ssl_ca_certs
                    })
            connection_pool = NewConnection(**kwargs)
        super(RedisConn,
              self).__init__(host=host,
                             port=port,
                             db=db,
                             password=password,
                             socket_timeout=socket_timeout,
                             socket_connect_timeout=socket_connect_timeout,
                             socket_keepalive=socket_keepalive,
                             socket_keepalive_options=socket_keepalive_options,
                             connection_pool=connection_pool,
                             unix_socket_path=unix_socket_path,
                             encoding=encoding,
                             encoding_errors=encoding_errors,
                             charset=charset,
                             errors=errors,
                             decode_responses=decode_responses,
                             retry_on_timeout=retry_on_timeout,
                             ssl=ssl,
                             ssl_keyfile=ssl_keyfile,
                             ssl_certfile=ssl_certfile,
                             ssl_cert_reqs=ssl_cert_reqs,
                             ssl_ca_certs=ssl_ca_certs)
