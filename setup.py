#!/usr/bin/env python
'''
Sentry-Pushsafer
=============
A [Sentry](https://www.getsentry.com/) plugin that sends notifications to [Pushsafer](https://www.pushsafer.com) registered device(s).

License
-------
Copyright 2018 Appzer.de Kevin Siml

This file is part of Sentry-Pushsafer.

Sentry-Pushsafer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''
from setuptools import setup, find_packages

setup(
    name='sentry-pushsafer',
    version='1.1.0',
    author='Kevin Siml',
    author_email='support@pushsafer.com',
    url='https://github.com/appzer/sentry-pushsafer',
    description='A Sentry plugin that integrates with pushsafer',
    long_description=__doc__,
    license='GPL',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'pushsafer = sentry_pushsafer.plugin:PushsaferNotifications'
        ]
    },
    include_package_data=True,
)
