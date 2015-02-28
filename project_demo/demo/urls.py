#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import test, demo


urlpatterns = patterns('',
                       url(r'^test/$', test, name='test'),
                       url(r'^demo/$', demo, name='debug'), )
