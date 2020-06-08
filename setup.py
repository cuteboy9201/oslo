#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: Youshumin
@Date: 2019-11-05 12:01:45
@LastEditors  : Youshumin
@LastEditTime : 2020-01-02 09:56:31
@Description: 
"""
from setuptools import setup

setup(
    name="oslo",
    version="1.0.2",
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
        "oslo.util",
    ],
    zip_safe=False,
    install_requires=[""],
)
