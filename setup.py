#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages, setup


import multifieldclean


setup(
    name='django_multifield_clean',
    version=multifieldclean.__version__,
    packages=find_packages(),
    author='Antoine Humeau',
    author_email='humeau.antoine@gmail.com',
    description='TODO',
    long_description=open('README.md').read(),
    include_package_data=True,
    url='TODO',
    classifiers=[  #TODO
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    license='TODO',
)
