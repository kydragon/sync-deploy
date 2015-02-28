#!usr/bin/env python
# coding: utf-8

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import os
from fabric.api import *
from config import env_ky, remote_folder
from common import MyUtilsOS
from update_collector import config_update_datetime, record_action_files


class SyncUpload():
    """自动发布基类.
    """

    def __init__(self):
        pass

    def __update_upload(self):
        u"""执行本地更新包的迭代操作.
        """

        # 配置起始点时间
        config_update_datetime(__file__)

        # 更新开始前
        self.upload_before()

        # 检索收集待上传文件
        with lcd(env_ky.app_path):  # 切换的自动部署脚本目录
            record_action_files()  # 检索更新文件，记录更新文件，以zip存档更新文件

        # 上传更新包文件到远程
        with lcd(env_ky.storage_path):  # 切换到更新包存档目录

            local('tar czf %s.tar.gz %s.zip' % (env_ky.gen_pkg_name, env_ky.gen_pkg_name))  # 压缩本地更新包
            put('%s.tar.gz' % env_ky.gen_pkg_name, remote_folder)  # 上传压缩包到远程目录

        # 远程文件解压覆盖
        with cd(remote_folder):  # 切换到远程目录
            run('tar zxf %s.tar.gz' % env_ky.gen_pkg_name)  # 远程解压
            run('unzip %s.zip' % env_ky.gen_pkg_name)  # 远程解压

            run('rm %s.tar.gz' % env_ky.gen_pkg_name)  # 远程删除
            run('rm %s.zip' % env_ky.gen_pkg_name)  # 远程删除

        # 更新完成后
        if env_ky.dynamic_file_exist:
            # 如果有动态文件, 重启web站点
            # 如果只是模板html, js, css, 图片等文件, 就勿需重启啦
            self.upload_after()

    def __update_rollback(self):
        u"""更新发布失败, 执行回滚.

            以项目的父级目录操作.
        """

        remote_project_parent_dir = os.path.dirname(remote_folder)

        # 上次发布前的备份文件
        bck_log = None
        try:
            bck_log = open('%s/backup_remote.log' % env_ky.app_path, 'rb')
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
        """上传前的工作
        """

        self.__backup_for_rollback()
        raise NotImplemented

    def upload_after(self):
        """上传后的工作
        """

        raise NotImplemented

    @staticmethod
    def __backup_for_rollback():
        u"""远程文件打包备份, 用户迭代失败的回滚.

            以项目的父级目录备份操作.
        """

        backup_project_file_name = "backup_%s.tar.gz" % env_ky.gen_pkg_name
        remote_project_parent_dir = os.path.dirname(remote_folder)

        # 远程文件打包备份
        with cd(remote_project_parent_dir):  # 切换到远程目录
            xx = MyUtilsOS.is_file_in_folder(remote_project_parent_dir)
            print xx
            run('tar -czf %s %s' % (backup_project_file_name, remote_folder))  # 远程项目打包备份

        # 远程备份记录
        # 这次发布前的备份文件
        with lcd(env_ky.app_path):
            local('echo %s >> backup_remote.log' % backup_project_file_name)

    @classmethod
    def upload(cls):
        u"""执行本地更新包的迭代操作.
        """
        cls.__update_upload()

    @classmethod
    def rollback(cls):
        u"""更新发布失败, 执行回滚.

            以项目的父级目录操作.
        """

        cls.__update_rollback()
