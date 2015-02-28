#!usr/bin/env python
# coding: utf-8

u"""
    自动化部署, 本地到远程任务.

    usage: fab update_upload -f fabric.py
"""

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

from sync_deploy import SyncUpload
from common import update_svn_windows, site_restart


class ProjectUpload(SyncUpload):
    """项目中实际自动上传类.
    """

    def upload_before(self):
        ProjectUpload.upload_before(self)
        update_svn_windows()

    def upload_after(self):
        ProjectUpload.upload_after(self)
        site_restart()


def update_upload():
    ProjectUpload().upload()


def update_rollback():
    u"""更新发布失败, 执行回滚.

        以项目的父级目录操作.
    """

    ProjectUpload().rollback()
