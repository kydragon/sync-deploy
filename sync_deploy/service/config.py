#!usr/bin/env python
# coding: utf-8

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import random
from time import time, strftime, localtime
from django.conf import settings
from common import AttributeDict

IGNORE_FOLDER = ('deploy',)  # 忽略掉某些指定文件夹
FILTER_TYPE = ('.pyo', '.pyc', '.js', '.css', '.html', '.gif', '.jpg', '.png')  # 查找哪些类型的文件


def generate_tmp_name():
    u"""生成当前日期+时间+随机数的文件名.
    """

    my_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    my_slice = ''.join(random.sample(my_list, 4))
    return '%s%s' % (strftime("%Y%m%d%H%M%S", localtime()), my_slice)


base_time = time()  # 起始时间，防止误操作，默认为当前时间
generate_name = generate_tmp_name()

# noinspection PyUnresolvedReferences
env_ky_dict = {
    'project_path': '',  # 当前项目搜索目标
    'storage_path': '',  # 生成文件存放路径

    'filter_type': FILTER_TYPE,  # 查找哪些类型的文件
    'ignore_folder': IGNORE_FOLDER,  # 忽略指定文件夹

    'base_time': base_time,  # 当前程序搜索起始日期
    'gen_pkg_name': generate_name,  # 生成文件的名称
    'dynamic_file_exist': None,  # 动态文件存在与否
    'remote_folder': '/opt/www/project'
}

custom_fabric_env = getattr(settings, "CUSTOM_FABRIC_ENV", None)
if custom_fabric_env:
    env_ky_dict.update(custom_fabric_env)

env_ky = AttributeDict(env_ky_dict)
