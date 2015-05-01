#!/usr/bin/env python

"""
Settings for a simple app that we'll use to run test.
"""


DEBUG = True,

INSTALLED_APPS = (
    'multifieldclean.tests.test_app',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    },
}

SECRET_KEY = '*'
