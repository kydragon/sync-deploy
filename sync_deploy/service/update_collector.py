#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

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
import os.path
from time import time, ctime

from sync_deploy.service.common import generate_name, ZFile
from sync_deploy.service.config import log, env_ky
from sync_deploy.backends import save_backend


class Collector(object):
    u"""最新更新的文件收集.
    """

    def __init__(self, base_time=time(), remote_backup=True):

        self._base_time = base_time,  # 当前程序搜索起始日期
        self._gen_pkg_name = generate_name()  # 生成更新包文件的名称
        self._backup_pkg_name = "backup_before_%s.tar.gz" % self._gen_pkg_name if remote_backup else ''

    @property
    def gen_pkg_name(self):
        return self._gen_pkg_name

    @property
    def backup_pkg_name(self):
        return self._backup_pkg_name

    def search_match_files(self, directory):
        u"""根据配置信息, 寻找匹配条件的文件.

            :param directory: 指定目录文件夹
        """

        file_paths = ''
        for i in os.listdir(directory):
            old_path = os.path.join(directory, i)
            if os.path.isdir(old_path):
                if not os.path.basename(old_path) in env_ky.ignore_folder:
                    file_paths = ''.join((file_paths, self.search_match_files(old_path)))
            else:
                ext_name = os.path.basename(old_path)
                mod_time = os.path.getmtime(old_path)
                ext_name = os.path.splitext(ext_name)[1].lower()

                if ext_name in env_ky.filter_type and mod_time > self._base_time:
                    if ext_name in ('.py', '.pyc') and not env_ky.dynamic_file_exist:
                        env_ky.dynamic_file_exist = True

                    file_paths = ''.join((file_paths, '%s\n' % old_path))
                    log.debug('%15f -------- %s' % (mod_time, ctime(mod_time)))

        return file_paths

    def record_action_files(self):
        u"""根据配置信息, 寻找匹配条件的文件, 写入内容到日志文件."""

        if not os.path.exists(env_ky.storage_path):
            os.makedirs(env_ky.storage_path)
        else:
            if os.path.ismount(env_ky.storage_path) or not os.path.isdir(env_ky.storage_path):
                log.error(u'亲, 指定的存储路径错误!')
                return

        log_name = os.path.join(env_ky.storage_path, '%s.log' % self._gen_pkg_name)
        log_msgs = self.search_match_files(env_ky.project_path)

        # 压缩zip归档
        zip_file = os.path.join(env_ky.storage_path, '%s.zip' % self._gen_pkg_name)
        files = log_msgs.splitlines()
        ZFile.create(zip_file, files, env_ky.project_path)

        # 写入到日志文件
        log_file = open(log_name, 'w')
        log_file.writelines(log_msgs)
        log_file.close()

    def save_sync_info(self):
        u"""记录该次的时间点, 作为下次的时间起点."""

        save_backend(self._gen_pkg_name, self._base_time, self._backup_pkg_name)


if __name__ == '__main__':
    u"""直接文件调用运行.
    """

    Collector().record_action_files()
