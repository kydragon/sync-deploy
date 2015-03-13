#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from django.contrib import admin
from sync_deploy.models import SyncInfo


class SyncInfoAdmin(admin.ModelAdmin):
    u"""自定义ModelAdmin.
    """

    list_display = ('id', 'pkg_name', 'bck_name', 'base_date', 'add_date', 'status', )

    ordering = ('-id',)
    list_filter = ('pkg_name', 'bck_name',)
    search_fields = ('pkg_name', 'base_date',)


admin.site.register(SyncInfo)
# admin.site.register(SyncInfo, SyncInfoAdmin)