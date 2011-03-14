#!/usr/bin/env python
#coding: utf-8
from distutils.core import setup
import sys

reload(sys).setdefaultencoding("UTF-8")

setup(
    name='django-mgpe',
    version='0.1.0',
    author='Ivan Petukhov',
    author_email='satels@gmail.com',
    packages=[
        'django_mgpe', 'django_mgpe.xml',
    ],
    license = 'MIT license',
    description = u'Приложение для работы с mgpe.ru.'.encode('utf8'),
    classifiers=(
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ),
)
