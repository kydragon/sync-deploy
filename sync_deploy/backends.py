#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import os
import os.path
from time import strftime, localtime
from sync_deploy import env_ky
from sync_deploy.models import SyncInfo


def file_save(base_time, backup_pkg_name):
    """更新时间, 备份文件保存在文档."""

    pkg_update_log = os.path.join(env_ky.project_path, 'update_upload.log')
    bck_remote_log = os.path.join(env_ky.project_path, 'backup_remote.log')

    # 记录这次发布前的时间点.
    friendly_datetime_string = strftime("%Y-%m-%d %H:%M:%S\n", localtime(base_time))
    os.system('echo %s >> %s' % (friendly_datetime_string, pkg_update_log))

    # 远程备份这次发布前的文件.
    os.system('echo %s >> %s' % (backup_pkg_name, bck_remote_log))


def data_base_save(pkg_name, base_time, backup_pkg_name):
    """更新时间, 备份文件保存在数据库."""

    SyncInfo.objects.create_sync_info(pkg_name=pkg_name, base_date=base_time, bck_name=backup_pkg_name)


save_backend = data_base_save
