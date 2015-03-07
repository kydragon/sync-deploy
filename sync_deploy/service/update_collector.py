#!usr/bin/env python
# coding: utf-8

u"""
    迭代发布更新文件三步骤：
        1, 递归当前根目录, 把指定日期后修改的文件全部找出.
        2, 将找出的文件, 按路径逐行记录入日志，并做出压缩包.
        3, 利用自动化脚本, SSH登陆, 上传压缩包, 解压跑, 重启.

    配置数据项:
        1, 同步只针对指定文件类型
        2, 同步忽略掉某些指定文件夹
"""

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import os
import sys
import six
import os.path
from datetime import datetime
from time import time, ctime, mktime, strptime, strftime, localtime

from common import ZFile
from config import env_ky

# 时间格式输入错误提醒文字
DATETIME_FORMAT_ERROR = \
    u"""
        亲, 指定的时间格式错误！
        usage format: %Y-%m-%d / %Y-%m-%d %H:%M:%S
        format demo: "2013-08-21 / 2013-08-21 09:50:35
    """


def config_update_datetime(filename):
    u"""获取出指定时间点, 该时间点将作为查找更新文件的起点.

        :param filename: 更新时间点记录文件

        时间优先级设置:
            [有文件, 有数据, 有适配最后行]
                1: 指定时间, 上次成功更新的时间, 间隔不定时间端迭代.

            [有文件, 无数据或无适配最后行]
                2: 当前日期的零点零分, 发布当天的更新, 日迭代用于测试.

            [系统默认]
                3: 当前日期+当前时间, 也是默认的设置, 主要为防止无意触发.(有文件,有数据)

            [无文件]
                4: None, 初始第一次操作, 整目录上传.
    """

    try:
        # 优先使用配置文件, 注意, ini文件编码为ansi,以及日期的规范性, 否则容易异常
        # config_file = os.path.join(env_ky.project_path, '*.ini')

        config_file = '%s.ini' % os.path.splitext(filename)[0]

        # 时间记录文件(新文件收集打包时间)
        global COLLECTOR_DATETIME_LOG_FILE
        COLLECTOR_DATETIME_LOG_FILE = config_file

        if os.path.exists(config_file):
            daytime = mktime(strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d'))  # NO2 ACTION

            collector_datetime_log = open(config_file, 'rb')
            lines = collector_datetime_log.readlines()

            if lines:
                # 从哪个时间开始更新, 格式可视化为: '2013-09-01','2013-09-01 12:00:00'
                from_update_time = str(lines[-1].replace("\n", ""))
                try:
                    # NO_01 ACTION
                    try:
                        env_ky.base_time = mktime(strptime(from_update_time, '%Y-%m-%d'))
                    except (TypeError, ValueError, Exception):
                        env_ky.base_time = mktime(strptime(from_update_time, '%Y-%m-%d %H:%M:%S'))
                except (TypeError, ValueError, Exception):
                    six.print_(DATETIME_FORMAT_ERROR)
                    env_ky.base_time = daytime
            else:
                env_ky.base_time = daytime
        else:
            env_ky.base_time = 0.0  # NO4 ACTION
    except Exception as e:

        six.print_(e)

        # C: 时间记录文件数据异常
        # 再次使用程序里设置, 如果异常, 使用默认当前时间.

        env_ky.base_time = time()  # NO3 ACTION

    six.print_('------------', u'更新起止时间：%s' % ctime(env_ky.base_time), '------------')


def search_match_files(directory):
    u"""根据配置信息, 寻找匹配条件的文件.

        :param directory: 指定目录文件夹
    """

    file_paths = ''
    for i in os.listdir(directory):
        old_path = os.path.join(directory, i)
        if os.path.isdir(old_path):
            if not os.path.basename(old_path) in env_ky.ignore_folder:
                file_paths = ''.join((file_paths, search_match_files(old_path)))
        else:
            ext_name = os.path.basename(old_path)
            mod_time = os.path.getmtime(old_path)
            ext_name = os.path.splitext(ext_name)[1].lower()

            if ext_name in env_ky.filter_type and mod_time > env_ky.base_time:
                if ext_name in ('.py', '.pyc') and not env_ky.dynamic_file_exist:
                    env_ky.dynamic_file_exist = True

                file_paths = ''.join((file_paths, '%s\n' % old_path))
                six.print_('%15f -------- %s' % (mod_time, ctime(mod_time)))

    return file_paths


def record_action_files():
    u"""根据配置信息, 寻找匹配条件的文件, 写入内容到日志文件."""

    if not os.path.exists(env_ky.storage_path):
        os.makedirs(env_ky.storage_path)
    else:
        if os.path.ismount(env_ky.storage_path) or not os.path.isdir(env_ky.storage_path):
            six.print_(u'亲, 指定的存储路径错误!')
            return

    six.print_('\n%15f -------- %s\n' % (env_ky.base_time, ctime(env_ky.base_time)))
    log_name = os.path.join(env_ky.storage_path, '%s.log' % env_ky.gen_pkg_name)
    log_msgs = search_match_files(env_ky.project_path)

    # 压缩zip归档
    zip_file = os.path.join(env_ky.storage_path, '%s.zip' % env_ky.gen_pkg_name)
    files = log_msgs.splitlines()
    ZFile.create(zip_file, files, env_ky.project_path)

    # 写入到日志文件
    log_file = open(log_name, 'w')
    log_file.writelines(log_msgs)
    log_file.close()

    # 记录该次的时间点, 作为下次的时间起点.
    friendly_datetime_string = strftime("%Y-%m-%d %H:%M:%S\n", localtime(env_ky.base_time))
    os.system('echo %s >> %s' % (friendly_datetime_string, COLLECTOR_DATETIME_LOG_FILE))


def console_running():
    u"""以控制台的形式传值运行, 主要作用是赋值时间点, 然后执行功能操作."""

    # 赋值时间点
    arg_num = len(sys.argv)

    if arg_num < 2:
        six.print_(u"请输入起始时间")
    else:
        str_format = '%Y-%m-%d'
        input_date = sys.argv[1]
        # six.print_(input_date

        if arg_num == 3:
            input_time = sys.argv[2]
            str_format = '%Y-%m-%d %H:%M:%S'
            input_date = '%s %s' % (input_date, input_time)
            # six.print_(input_time, input_date

        try:
            env_ky.base_time = mktime(strptime(input_date, str_format))
        except (TypeError, ValueError, Exception):
            six.print_(DATETIME_FORMAT_ERROR)

    # 执行功能操作
    record_action_files()


if __name__ == '__main__':
    u"""直接文件调用运行.
    """

    # six.print_(env_ky.storage_path)
    record_action_files()
    # console_running()

    pass
