#!/usr/bin/env python
# coding: utf-8

u"""
    递归更改一个目录下的所有文件名为小写.

    usage:
        from lower2upper import lower_file_name
"""

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import os
import sys
import six
import os.path


def lower_file_name(directory):
    u"""递归更改目录文件名大小写.
    """

    if not os.path.exists(directory) or not os.path.isdir(directory):
        six.print_(u"无效的目录")
        return

    for i in os.listdir(directory):
        lower_name = i.lower()
        old_path = os.path.join(directory, i)
        new_path = os.path.join(directory, lower_name)
        six.print_('%s : %s -----> %s' % (old_path, i, lower_name))

        if os.path.isdir(old_path):
            lower_file_name(old_path)
        else:
            os.rename(old_path, new_path)


if __name__ == '__main__':
    u"""单元测试.
    """

    arg_num = len(sys.argv)
    if arg_num < 2:
        six.print_(u'请输入目录名')
    else:
        file_dir = sys.argv[1]
        lower_file_name(file_dir)
