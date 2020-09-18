#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: YouShumin
Date: 2020-09-08 16:45:57
LastEditTime: 2020-09-17 17:21:46
LastEditors: YouShumin
Description: Another flat day
FilePath: /oslo/setup.py
'''
from setuptools import setup

setup(
    name="oslo",
    version="1.0.3",
    author="youshumin",
    author_email="ysm0119@126.com",
    url="https://github.com/cuteboy9201/oslo",
    packages=[
        "oslo",
        "oslo.web",
        "oslo.db",
        "oslo.form",
        "oslo.task",
        "oslo.http",
        "oslo.utils",
    ],
    zip_safe=False,
    install_requires=[""],
)
