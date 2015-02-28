#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""强制编译项目源代码文件到pyc.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'

import os

from django.utils.importlib import import_module
from django.core.management.base import NoArgsCommand

from sync_deploy.service.rename_lower import lower_file_name


class Command(NoArgsCommand):
    help = "rename project files to lower case."

    def handle_noargs(self, **options):
        setting_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        project_catalog = os.path.dirname(os.path.dirname(import_module(setting_module).__file__))

        lower_file_name(project_catalog)
