#!usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

u"""代码工具箱
"""

__author__ = 'kylinfish@126.com'
__date__ = '2013/8/15'

import os
import zipfile
import random
from time import strftime, localtime
from sync_deploy.service.config import log


def generate_name():
    u"""生成当前日期+时间+随机数的文件名.
    """

    my_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    my_slice = ''.join(random.sample(my_list, 4))
    return '%s%s' % (strftime("%Y%m%d%H%M%S", localtime()), my_slice)


class MyUtilsOS(object):
    """自定义的os工具集.
    """

    @classmethod
    def is_file_in_folder(cls, folder_path):
        """判断目录是否有实际文件.

            :param folder_path 目录
        """

        # 设置文件夹内容是否为空标识符
        empty = False

        for root, dirs, files in os.walk(folder_path):
            if files:
                empty = True
                break

            for each_dir in dirs:
                empty = cls.is_file_in_folder(each_dir)

        return empty

    @classmethod
    def rm_file_in_folder(cls, folder_path):
        """删除目录是否有实际文件.

            :param folder_path 目录
        """

        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return

        for root, dirs, files in os.walk(folder_path):
            if dirs:
                for each_dir in dirs:
                    cls.rm_file_in_folder(os.path.join(folder_path, each_dir))

            if files:
                for each_file in files:
                    os.remove(os.path.join(folder_path, each_file))

        os.rmdir(folder_path)

    @staticmethod
    def mk_folder(folder_path, mode='d'):
        """创建文件或目录.

            :param folder_path 目录或文件
        """

        if os.path.exists(folder_path):
            return

        if mode == 'd':
            os.mkdir(folder_path)
        elif mode == 'f':
            os.mkfifo(folder_path)

    @staticmethod
    def test_utils():
        """测试.
        """

        # noinspection PyUnresolvedReferences
        test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')

        MyUtilsOS.rm_file_in_folder(test_path)
        MyUtilsOS.mk_folder(test_path)
        log.debug(MyUtilsOS.is_file_in_folder(test_path))

        # 创建空子目录判断
        for i in range(5):
            MyUtilsOS.mk_folder(os.path.join(test_path, str(i)))
        log.debug(MyUtilsOS.is_file_in_folder(test_path))

        # 根目录创建文件判断
        MyUtilsOS.mk_folder(os.path.join(test_path, 'w'), 'f')
        log.debug(MyUtilsOS.is_file_in_folder(test_path))

        # 子目录创建文件判断
        os.remove(os.path.join(test_path, 'w'))
        MyUtilsOS.mk_folder(os.path.join(test_path, '0', 'w'), 'f')
        log.debug(MyUtilsOS.is_file_in_folder(test_path))


class ZFile(object):
    u"""zip文件压缩与解压处理.
    """

    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zip_file = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zip_file = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)

    def addfile(self, path, arc_name=None):
        path = path.replace('//', '/')
        if not arc_name:
            if path.startswith(self.basedir):
                # log.debug(path, '|', self.basedir)
                arc_name = path[len(self.basedir):]
            else:
                arc_name = ''
        self.zip_file.write(path, arc_name)

    def add_files(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)

    def close(self):
        self.zip_file.close()

    def extract_to(self, path):
        for p in self.zip_file.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir_path = os.path.dirname(f)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            file(f, 'wb').write(self.zip_file.read(filename))

    @staticmethod
    def create(zip_file_name, files, basedir=''):
        u"""创建压缩文件.
        """

        z = ZFile(zip_file_name, 'w', basedir)
        z.add_files(files)
        z.close()

    @staticmethod
    def extract(zip_file_name, path, basedir=''):
        u"""提取压缩文件.
        """

        z = ZFile(zip_file_name, basedir)
        z.extract_to(path)
        z.close()


class AttributeDict(dict):
    u"""
        Dictionary subclass enabling attribute lookup/assignment of keys/values.
        自定义字典子类, 支持属性键值(key-value)形式查找和赋值.
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def first(self, *keys):
        u"""取列表键里取出一个键的值.

            :type keys: 列表键
        """
        for key in keys:
            value = self.get(key, None)
            if value:
                return value

    @staticmethod
    def test_attribute_dict():
        u"""测试自定义字典类.
        """

        env_ky_a = AttributeDict(key_a=1, key_b=2)
        log.debug(env_ky_a.key_a, '---|---', env_ky_a.key_b)

        env_ky_dict = {'key_A': 11, 'key_B': 12}
        env_ky_b = AttributeDict(env_ky_dict)
        log.debug(env_ky_b.key_A, '---|---', env_ky_b.key_B)


if __name__ == '__main__':
    u"""测试.
    """

    # AttributeDict.test_attribute_dict()
    MyUtilsOS.test_utils()

    # pass
