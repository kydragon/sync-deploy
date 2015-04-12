#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

u"""读取存放测试脚本的文件, 以命令行的形式执行指定的行脚本, 指定范围的行脚本.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'

import os
from django.conf import settings
from django.utils.importlib import import_module
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "execute curl command script in saved file."

    def handle_noargs(self, **options):
        setting_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        project_catalog = os.path.dirname(os.path.dirname(import_module(setting_module).__file__))

        # noinspection PyUnresolvedReferences
        upload_config = getattr(settings, "CUSTOM_FABRIC_MODULE", None)
        rollback_method = getattr(settings, "CUSTOM_FABRIC_ROLLBACK", None)

        if upload_config and rollback_method:
            paths = '/'.join(upload_config.split('.'))
            fabric_file = os.path.join(project_catalog, paths)

            os.system("fab -f %s.py %s" % (fabric_file, rollback_method))
