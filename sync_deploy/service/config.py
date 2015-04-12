#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import logging
from django.conf import settings
from sync_deploy.service.common import AttributeDict

logging.basicConfig()

log = logging.getLogger("sync_deploy")
log.setLevel(logging.DEBUG)

# 查找哪些类型的文件
FILTER_TYPE = ('.pyo', '.pyc', '.js', '.css', '.html', '.gif', '.jpg', '.png')

# noinspection PyUnresolvedReferences
env_ky_dict = {
    'project_path': '',  # 当前项目搜索目标
    'storage_path': '',  # 生成文件存放路径

    'filter_type': FILTER_TYPE,  # 查找哪些类型的文件
    'ignore_folder': None,  # 忽略指定文件夹

    'dynamic_file_exist': None,  # 动态文件存在与否
    'remote_folder': '/opt/www/project'
}

custom_fabric_env = getattr(settings, "CUSTOM_FABRIC_ENV", None)
if custom_fabric_env:
    env_ky_dict.update(custom_fabric_env)

env_ky = AttributeDict(env_ky_dict)
