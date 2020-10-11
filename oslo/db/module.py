#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-06 09:08:58
LastEditors: YouShumin
LastEditTime: 2020-10-10 15:26:31
@Description: 
'''
import logging
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback
LOG = logging.getLogger(__name__)


class DBPool(object):
    def __init__(self):
        self.subdb = defaultdict(list)

    def add(self, dbname, db):
        self.subdb[dbname].append(db)

    def remove(self, dbname, db):
        self.subdb[dbname].remove(db)

    def get(self, dbname):
        return self.subdb[dbname]


db_pool = DBPool()


class mysqlHanlder(object):
    def init(self, dbname=None, dburl=None, dbecho=False, pool_size=10):
        LOG.info("dbname: {}, dburl: {}".format(dbname, dburl))
        self.db_name = dbname
        self.db_url = dburl
        self.db_echo = dbecho
        self.db_pool_size = pool_size
        self._check_db_name()

    def _check_db_name(self):
        resp = db_pool.get(self.db_name)
        if not resp:
            self._init_engin()
            self._init_session()
            db_pool.add(self.db_name, [self.session, self.engin])

    def _init_engin(self):
        self.engin = create_engine(self.db_url,
                                   encoding="utf-8",
                                   echo=self.db_echo,
                                   pool_size=self.db_pool_size,
                                   pool_recycle=3600,
                                   pool_pre_ping=True)

    def _init_session(self):
        self.session = scoped_session(
            sessionmaker(bind=self.engin, expire_on_commit=False))

    def get_session(self, db_name):
        if not db_name:
            return ""
        db_list = db_pool.get(db_name)
        if db_list:
            db = db_list[0][0]
            return db()
        else:
            LOG.error("get_db: {} faild".format(db_name))
        return ""

    def get_engin(self, db_name):
        db_list = db_pool.get(db_name)
        if db_list:
            db = db_list[0][1]
            return db
        else:
            LOG.error("get_db: {} faild".format(db_name))
        return ""


class MixDbBase:
    def __init__(self, db_name="", table=""):
        self.table = table
        self.session = self.create_db_engin(db_name=db_name)
        self.db_obj = self.session.query(self.table)

    # 创建数据库engin
    def create_db_engin(self, db_name=None):
        return mysqlHanlder().get_session(db_name=db_name)

    # 获取数据库对象
    def get_db(self, **kwargs):
        return self.db_obj.filter_by(**kwargs)

    # 获取一条信息 根据ID
    def getById(self, id):
        return self.get_db(id=id).first()

    # 修改一条信息 根据ID
    def putById(self, id, **kwargs):
        db = self.get_db(id=id)
        if db:
            db.update({**kwargs})
            self.session.commit()
            return True, id
        else:
            False, "ID不存在"

    # 增加一条信息根据ID
    def addById(self, id, **kwargs):
        db = self.get_db(id=id)
        if not db:
            add_data = self.table(id=id, **kwargs)
            self.session.add(add_data)
            self.session.commit()
            return True, id
        else:
            return False, "已经存在"
        db = self.get_db(id=id)
        if db:
            return False, "已经存在"
        try:
            add_data = self.table(id=id, **kwargs)
            self.session.add(add_data)
            self.session.commit()
            return True, id
        except Exception as e:
            LOG.debug(str(e))
            LOG.error(traceback.format_exc())
            self.session.rollback()
            return False,"未知错误"

    # 根据ID删除一条信息
    def delById(self, id):
        db = self.get_db(id=id)
        if db:
            try:
                self.session.delete(db.first())
                self.session.commit()
                return True
            except Exception as e:
                LOG.debug(str(e))
                LOG.error(traceback.format_exc())
                self.session.rollback()
                return False
        else:
            return False
    
    def get_info(self, **kwargs):
        return self.get_db(**kwargs).all()

    def __del__(self):
        self.session.close()