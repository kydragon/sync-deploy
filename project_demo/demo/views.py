# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse


def test(request):
    u"""
    """

    error = 9999
    if request.method != 'POST':
        return HttpResponse({'error': error})


def demo(request):
    u"""
    """

    result_data = []

    for (key, value) in request.POST.items():
        result_data.append(value)

    return HttpResponse({'error': 0, 'data': result_data})  # ok, success.
