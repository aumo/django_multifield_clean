#!/usr/bin/env python
# coding: utf-8

'''
Simple helper to handle settings and their defaults.
'''

from django.conf import settings


DEFAULTS = {
    'METHOD_PREFIX': 'multi_clean',
}


def setting(name):
    return getattr(
        settings,
        'MULTIFIELD_CLEAN_{}'.format(name),
        DEFAULTS[name]
    )
