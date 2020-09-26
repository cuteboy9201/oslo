#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: YouShumin
Date: 2020-09-26 15:54:01
LastEditTime: 2020-09-26 19:12:28
LastEditors: YouShumin
Description: Another flat day
FilePath: /oslo/oslo/db/cache_redis.py
'''
import redis 
import pickle
import logging 
import inspect
import hashlib
from redis import connection
from redis.sentinel import SentinelConnectionPool, Sentinel
from tornado import gen 
from oslo.db.dredis import NewRedisPool
from collections import defaultdict

LOG = logging.getLogger(__name__)

class __RedisPools(object):

    def __init__(self):
        self.subdb = defaultdict(list)

    def add(self, dbname, db):
        self.subdb[dbname] = db
    # def remove(self, dbname, db):
    #     self.subdb[dbname].remove(db)

    def get(self, dbname):
        return self.subdb[dbname]

    def get_list(self):
        return list(self.subdb.values())
    
    def get_pool(self):
        return self.subdb

_CONN = {}
_redis_pools = __RedisPools()
class __RedisHandler(object):

    def init(self, db_key_name="default_redis_name", db_host=None, db_port=None,is_sentinel=False, sentinel_host=None, ttl=3600, db=10):
        self.db_key_name = db_key_name
        self.db_host = db_host
        self.db_port = db_port
        self.is_sentinel =is_sentinel
        self.sentinel_host = sentinel_host
        self.db = db
        if not self.is_sentinel:
            self.rid = self.db_key_name
            self.set_redis_connnect()
        else:
            self.rid= ""

    def set_redis_connnect(self):
        socket_timeout = 0.1
        redis_config = dict(
            host=self.db_host, port=self.db_port, db=self.db, socket_timeout=socket_timeout
        )
        _redis_pools.add(self.db_key_name, NewRedisPool(**redis_config))
    
    def get_redis_conn(self, key=None, rid=None):
        if key is not None and not self.is_sentinel:
            key_hash = hash(key)
            key_num = key_hash % 10
            redis_pool = _redis_pools.get_list()
            pool = redis_pool[key_num % len(redis_pool)]
        else:
            key_num= "1"
            pool = None
            pass 
            # sentinel处理 
        if key_num in _CONN:
            return _CONN[key_num]
    
        conn = redis.StrictRedis(connection_pool=pool)
        _CONN[key_num] = conn 
        return conn

    def pickle_loads(self,data):
        try:
            return pickle.loads(data)
        except Exception as ex:
            logging.warning('[rCache]cPickle loads %s' % repr(ex))
            return None

    def get_cache(self, key, rid=None):
        if not self.rid:
            rid = self.slave_key
        conn = self.get_redis_conn(key=key, rid=rid)
        r_data = conn.get(key)
        if r_data:
            return self.pickle_loads(r_data)
        return None

    def set_cache(self,key, data, ttl=3600, rid=None):
        rid = self.rid if self.rid else self.master_key
        conn = self.get_redis_conn(key=key, rid=rid)
        data = pickle.dumps(data)
        if ttl:
            return conn.setex(key, ttl, data)
        return conn.set(key, data)         

REDIS = __RedisHandler()

if __name__ == "__main__":
    import sys 
    sys.path.insert(0,"/Users/youshumin/Desktop/code/")
    REDIS.init(db_key_name="123", db_host="192.168.2.34", db_port=20011)
    REDIS.set_cache("youshumin","ddasdfasdf")
    data = REDIS.get_cache("youshumin")
    print(data)