#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

u"""编译项目源代码文件到pyc.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'

import os
import compileall
from django.utils.importlib import import_module
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "compile project code files."

    def handle_noargs(self, **options):
        setting_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        project_catalog = os.path.dirname(os.path.dirname(import_module(setting_module).__file__))

        compileall.compile_dir(project_catalog, force=0, quiet=0)
