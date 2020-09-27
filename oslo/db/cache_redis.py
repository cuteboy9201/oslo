#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: YouShumin
Date: 2020-09-26 15:54:01
LastEditTime: 2020-09-27 19:08:40
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

    def get(self, dbname):
        return self.subdb[dbname]

    def get_list(self):
        return list(self.subdb.values())

    def get_pool(self):
        return self.subdb


_CONN = {}
_redis_pools = __RedisPools()


class __RedisHandler(object):
    def init(self,
             db_key_name="default_redis_name",
             db_host=None,
             db_port=None,
             is_sentinel=False,
             sentinel_host=None,
             ttl=3600,
             db=10):
        self.db_key_name = db_key_name
        self.db_host = db_host
        self.db_port = db_port
        self.is_sentinel = is_sentinel
        self.sentinel_host = sentinel_host
        self.db = db
        if not self.is_sentinel:
            self.rid = self.db_key_name
            self.set_redis_connnect()
        else:
            self.rid = ""

    def set_redis_connnect(self):
        socket_timeout = 0.1
        redis_config = dict(host=self.db_host,
                            port=self.db_port,
                            db=self.db,
                            socket_timeout=socket_timeout)
        _redis_pools.add(self.db_key_name, NewRedisPool(**redis_config))

    def get_redis_conn(self, key=None, rid=None):
        if key is not None and not self.is_sentinel:
            key_hash = hash(key)
            key_num = key_hash % 10
            redis_pool = _redis_pools.get_list()
            pool = redis_pool[key_num % len(redis_pool)]
        else:
            key_num = "1"
            pool = None
            pass
            # sentinel处理
        if key_num in _CONN:
            return _CONN[key_num]

        conn = redis.StrictRedis(connection_pool=pool)
        _CONN[key_num] = conn
        return conn

    def pickle_loads(self, data):
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

    def set_cache(self, key, data, ttl=3600, rid=None):
        rid = self.rid if self.rid else self.master_key
        conn = self.get_redis_conn(key=key, rid=rid)
        data = pickle.dumps(data)
        if ttl:
            return conn.setex(key, ttl, data)
        return conn.set(key, data)

    def del_cache(self, key, rid=None):
        rid = self.rid if self.rid else self.master_key
        self.get_redis_conn(key=key, rid=rid).delete(key)


REDIS = __RedisHandler()


class SyncCache:
    def __init__(self,
                 key=None,
                 ttl=60 * 60,
                 pass_args=0,
                 prefix_key="_default"):
        self.prefix_key = prefix_key
        self.key = prefix_key + key
        self.ttl = ttl
        self.pass_args = pass_args

    def __call__(self, func):
        self.func = func
        farg = inspect.getargspec(func).args[:1]
        self.skip_self_args = True if farg and (farg[0] == "self"
                                                or farg[0] == "cls") else False

        def deco_func(*args, **kwargs):
            return self.call_func(*args, **kwargs)

        setattr(deco_func, "del_cache", self._del_cache)
        setattr(deco_func, "clr_cache", self._clr_cache)
        return deco_func

    def gen_key(self, prefix, args, kwargs):
        key = prefix + ",".join([i for i in args]) \
                    + ",".join([a + str(b)
                                for a, b in kwargs.items()])
        if len(key) > 200:
            key = key.ecode("utf8")
            key = prefix + hashlib.md5(key).hexdigest
        return key

    def _gen_key(self, *args, **kwargs):
        par = self.pass_args if not self.skip_self_args else max(
            self.pass_args, 1)
        return self.gen_key("%s.%s" % (self.prefix_key, self.func.__name__),
                            args[par:], kwargs)

    def call_func(self, *args, **kwargs):
        LOG.debug("get_cache: args: {}, kwargs: {}".format(args, kwargs))
        key = self._gen_key(*args, **kwargs)
        ret = REDIS.get_cache(key)
        if ret is not None:
            return ret
        ret = self.func(*args, **kwargs)
        REDIS.set_cache(key=key, data=ret, ttl=self.ttl)
        return ret

    def _del_cache(self, *args, **kwargs):
        LOG.debug("del_one_redis: args: {}, kwargs: {}".format(args, kwargs))
        k = self._gen_key(*args, **kwargs)
        REDIS.del_cache(key=k)

    def _clr_cache(self, *args, **kwargs):
        LOG.debug("del_all_redis: args: {}, kwargs: {}".format(args, kwargs))
        kp = self.gen_key(self.prefix_key + "*", args, kwargs)
        wc = REDIS.get_redis_conn(key=kp)
        keys = [k for k in wc.scan_iter(kp)]
        if keys:
            wc.delete(*keys)

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/Users/youshumin/Desktop/code/")
    REDIS.init(db_key_name="123", db_host="192.168.2.34", db_port=20011)
    REDIS.set_cache("youshumin", "ddasdfasdf")
    data = REDIS.get_cache("youshumin")
    print(data)