#!usr/bin/env python
# coding: utf-8

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import os
from fabric.api import *
from sync_deploy.models import SyncInfo
from sync_deploy.service.config import env_ky
from sync_deploy.service.common import MyUtilsOS
from sync_deploy.service.update_collector import Collector


class SyncUpload(object):
    """自动发布基类.
    """

    def __init__(self):
        latest_datetime = SyncInfo.objects.get_latest_datetime()
        if latest_datetime:
            self._collector = Collector(base_time=latest_datetime)
        else:
            self._collector = Collector()

    def __update_upload(self):
        u"""执行本地更新包的迭代操作."""

        # 更新开始前
        self.upload_before()

        # 检索收集待上传文件
        with lcd(env_ky.project_path):  # 切换的自动部署脚本目录
            self._collector.record_action_files()  # 检索更新文件，记录更新文件，以zip存档更新文件

        # 上传更新包文件到远程
        with lcd(env_ky.storage_path):  # 切换到更新包存档目录

            local('tar czf %s.tar.gz %s.zip' % (self._collector.gen_pkg_name, self._collector.gen_pkg_name))  # 压缩本地更新包
            put('%s.tar.gz' % self._collector.gen_pkg_name, env_ky.remote_folder)  # 上传压缩包到远程目录

        # 远程文件解压覆盖
        with cd(env_ky.remote_folder):  # 切换到远程目录
            run('tar zxf %s.tar.gz' % self._collector.gen_pkg_name)  # 远程解压
            run('unzip %s.zip' % self._collector.gen_pkg_name)  # 远程解压

            run('rm %s.tar.gz' % self._collector.gen_pkg_name)  # 远程删除
            run('rm %s.zip' % self._collector.gen_pkg_name)  # 远程删除

        # 更新完成后
        if env_ky.dynamic_file_exist:
            # 如果有动态文件, 重启web站点
            # 如果只是模板html, js, css, 图片等文件, 就勿需重启啦
            self.upload_after()

    def __update_rollback(self):
        u"""更新发布失败, 执行回滚, 以项目的父级目录操作."""
        remote_project_parent_dir = os.path.dirname(env_ky.remote_folder)

        # 上次发布前的备份文件
        bck_log = None
        try:
            bck_log = open('%s/backup_remote.log' % env_ky.project_path, 'rb')
            # 取文件记录的最后一行
            backup_project_file_name = str(bck_log.readlines()[-1].replace("\n", ""))
        except:
            raise
        finally:
            if bck_log:
                bck_log.close()

        # 远程文件解压覆盖
        with cd(remote_project_parent_dir):  # 切换到远程目录
            run('tar zxf %s' % backup_project_file_name)  # 远程解压
            run('rm %s' % backup_project_file_name)  # 远程删除

        # 完成后重启
        self.upload_after()

    def upload_before(self):
        """上传前的工作."""
        self.__backup_for_rollback()

    def upload_after(self):
        """上传后的工作."""
        pass

    def __backup_for_rollback(self):
        u"""远程文件打包备份, 用户迭代失败的回滚, 以项目的父级目录备份操作."""
        backup_project_file_name = "backup_%s.tar.gz" % self._collector.gen_pkg_name
        remote_project_parent_dir = os.path.dirname(env_ky.remote_folder)

        # 远程文件打包备份
        with cd(remote_project_parent_dir):  # 切换到远程目录
            MyUtilsOS.is_file_in_folder(remote_project_parent_dir)
            run('tar -czf %s %s' % (backup_project_file_name, env_ky.remote_folder))  # 远程项目打包备份

        # 远程备份记录, 这次发布前的备份文件.
        with lcd(env_ky.project_path):
            local('echo %s >> backup_remote.log' % backup_project_file_name)

    def upload(self):
        u"""执行本地更新包的迭代操作."""
        self.__update_upload()

    def rollback(self):
        u"""更新发布失败, 执行回滚, 以项目的父级目录操作."""
        self.__update_rollback()
