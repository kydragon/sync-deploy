#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""SyncInfo data model.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/22'

from django.db import models
from django.utils.translation import ugettext_lazy as _


class DataManager(models.Manager):
    u"""更新记录信息.
    """

    def get_latest_datetime(self):
        u"""ss
        """
        sync_info = None
        try:
            sync_info = self.last()
        except SyncInfo.DoesNotExist:
            pass
        except SyncInfo.MultipleObjectsReturned:
            pass
        return sync_info['add_date']

    def get_pkg_name(self, pkg_name):
        u"""更新记录信息项

            :param pkg_name: 更新包
        """

        sync_info = None
        try:
            sync_info = self.get(pkg_name=pkg_name)
        except SyncInfo.DoesNotExist:
            pass
        except SyncInfo.MultipleObjectsReturned:
            pass
        return sync_info

    def sync_info_exists(self, pkg_name):
        u"""判断更新记录是否存在.

            :param pkg_name: 更新包
        """

        sync_info = self.get_pkg_name(pkg_name=pkg_name)
        if sync_info:
            return True
        else:
            return False

    def create_sync_info(self, pkg_name):
        u"""更新记录信息添入.

            :param pkg_name: 更新包
        """

        sync_info = self.model(pkg_name=pkg_name)
        sync_info.save(using=self._db)

        return sync_info


class SyncInfo(models.Model):
    u"""更新记录信息.
    """

    id = models.AutoField(primary_key=True, verbose_name=_('auto ID'))
    pkg_name = models.CharField(_('pkg_name'), max_length=30, unique=True)
    add_date = models.DateTimeField(_('insert datetime'), auto_now_add=True)
    status = models.BooleanField(_('status'), default=True)

    objects = DataManager()

    class Meta:
        db_table = 'sync_deploy'
        verbose_name = _('deploy info')
        verbose_name_plural = _('deploy info list')

    def __unicode__(self):
        return "%s" % self.natural_key()

    def natural_key(self):
        return self.gen_pkg_name

    def update_info(self, **dicts):
        u"""设置并更新指定字段的值

            :param dicts
        """

        for (key, value) in dicts.items():
            if hasattr(self, key):
                setattr(self, key, value)
