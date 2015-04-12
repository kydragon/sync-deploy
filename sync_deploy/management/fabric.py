#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from fabric import state
from fabric.network import disconnect_all
from fabric.tasks import execute
from fabric.utils import abort
from fabric.main import find_fabfile, load_settings


def main(fab_file, cmd_name):
    """执行指定文件的指定命令.
    """
    try:
        state.env.update(load_settings(state.env.rcfile))
        fab_path = find_fabfile(fab_file)
        if not fab_path:
            abort("""Couldn't find any fab files!""")

        state.env.real_fabfile = fab_path
        execute(cmd_name)

        if state.output.status:
            print("\nDone.")
    except Exception, ex:
        print(ex)
    finally:
        disconnect_all()
