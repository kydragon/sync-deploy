#!usr/bin/env python
# coding: utf-8

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import os
import sys
import six
import random
import os.path

from time import time, strftime, localtime

from common import AttributeDict


# 起始时间，防止误操作，默认为当前时间
base_time = time()

# 当前执行文件存放路径
app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 当前文件物理路径的父父目录
project_path = os.path.dirname(app_path)

sys.path.append("..")

# 忽略掉某些指定文件夹
ignore_folder = ('deploy',)

# 查找哪些类型的文件
filter_type = ('.pyo', '.pyc', '.js', '.css', '.html', '.gif', '.jpg', '.png')


def generate_tmp_name():
    u"""生成当前日期+时间+随机数的文件名.
    """

    my_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    my_slice = ''.join(random.sample(my_list, 4))
    return '%s%s' % (strftime("%Y%m%d%H%M%S", localtime()), my_slice)


generate_name = generate_tmp_name()

# noinspection PyUnresolvedReferences
env_ky_dict = {
    'base_time': base_time,  # 当前程序搜索起始日期
    # 'app_path': app_path,  # 当前应用系统路径
    # 'project_path': project_path,  # 当前项目搜索目标
    'filter_type': filter_type,  # 查找哪些类型的文件
    'ignore_folder': ignore_folder,  # 忽略指定文件夹
    'gen_pkg_name': generate_name,  # 生成文件的名称
    'storage_path': os.path.join(app_path, r'archives'),  # 生成文件存放路径
    'dynamic_file_exist': None,  # 动态文件存在与否
}

env_ky = AttributeDict(env_ky_dict)

remote_folder = '/opt/www/project'

if __name__ == '__main__':
    u"""测试.
    """

    six.print_(env_ky.storage_path)
    # pass