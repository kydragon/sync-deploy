#!usr/bin/env python
# coding: utf-8

u"""
    fabric 环境变量参数配置.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

from fabric.api import env

env.user = 'kylin'
env.hosts = ['kylin@192.168.1.100', ]
env.passwords = {'kylin@192.168.1.100': '123456', }
