#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: Youshumin
@Date: 2019-11-05 12:01:45
@LastEditors: Youshumin
@LastEditTime: 2019-11-05 14:55:04
@Description: 
'''
from setuptools import setup

setup(
    name="oslo",
    version="1.0.0",
    author="youshumin",
    author_email="ysm0119@126.com",
    # description="",
    # url="",
    packages=["oslo", "oslo.web"],
    zip_safe=False,
    # include_package_data=True,
    install_requires=["tornado==4.3", ],
)
