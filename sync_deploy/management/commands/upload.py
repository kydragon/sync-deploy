#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

u"""对拦截curl记录保存文件, 做处理去掉重复行.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'

import os
from django.conf import settings
from django.utils.importlib import import_module
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = u"对拦截curl记录保存文件, 做处理去掉重复行."

    def handle_noargs(self, **options):
        setting_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        project_catalog = os.path.dirname(os.path.dirname(import_module(setting_module).__file__))

        # noinspection PyUnresolvedReferences
        upload_config = getattr(settings, "CUSTOM_FABRIC_MODULE", None)
        upload_method = getattr(settings, "CUSTOM_FABRIC_UPLOAD", None)

        if upload_config and upload_method:
            paths = '/'.join(upload_config.split('.'))
            fabric_file = os.path.join(project_catalog, paths)

            print("fab -f %s.py %s" % (fabric_file, upload_method))
            main(fab_file=fabric_file, cmd_name=upload_method)
            os.system("fab -f %s.py %s" % (fabric_file, upload_method))
