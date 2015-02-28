#!usr/bin/env python
# coding: utf-8

u"""自动化部署, 本地到远程任务前后动作."""

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

from fabric.api import *
from sync_deploy import env_ky
from config import svn_url


def update_svn_windows():
    u"""如果项目使用windows平台下SVN, 发布前获取下更新.
    """

    # 注意: win下将svn增加到环境path中
    # 比如: D:\Program Files\TortoiseSVN\bin
    # TortoiseSVN 命令参考其帮助文档

    # 切换到项目源码目录
    with lcd(env_ky.project_path):
        # 从SVN地址更新项目源码
        local('TortoiseProc.exe /command:update /url:%s /path:%s /closeonend:1' % (svn_url, env_ky.project_path))


def site_restart():
    u"""site restart."""

    # python: nginx + uwsgi
    sudo('invoke-rc.d uwsgi restart')
    sudo('nginx -s reload')
    sudo('service nginx restart')


def sys_update():
    u"""system update.
    """

    run('apt-get update')
    run('apt-get upgrade')


def my_command(str_cmd):
    u"""执行指定命令, 一定要引号引住.
    """

    run(str_cmd)
