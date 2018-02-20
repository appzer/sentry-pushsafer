#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Sentry-Pushsafer
=============

License
-------
Copyright 2018 Appzer.de Kevin Siml

This file is part of Sentry-Pushsafer.

Sentry-Pushsafer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
'''

from django import forms
import logging
from sentry.conf import settings
from sentry.plugins import Plugin

import sentry_pushsafer
import requests


class PushsaferSettingsForm(forms.Form):

    privatekey = forms.CharField(help_text='Your Private or Alias key. See https://www.pushsafer.com/')
    device = forms.CharField(help_text='Device or Device Group ID. See https://www.pushsafer.com/en/pushapi')
	icon = forms.CharField(help_text='Icon ID (optional, 1-176). See https://www.pushsafer.com/en/pushapi')
	iconcolor = forms.CharField(help_text='Icon Color (optional, Hexadecimal Colorcode, Example: #FF0000). See https://www.pushsafer.com/en/pushapi')
	sound = forms.CharField(help_text='Sound ID (optional, 0-50). See https://www.pushsafer.com/en/pushapi')
	vibration = forms.CharField(help_text='Vibration (optional, empty or 1-3). See https://www.pushsafer.com/en/pushapi')
	time2live = forms.CharField(help_text='Time to Live (optional, 0-43200: Time in minutes, after which message automatically gets purged.). See https://www.pushsafer.com/en/pushapi')

    choices = ((logging.CRITICAL, 'CRITICAL'), (logging.ERROR, 'ERROR'), (logging.WARNING,
               'WARNING'), (logging.INFO, 'INFO'), (logging.DEBUG, 'DEBUG'))
    severity = forms.ChoiceField(choices=choices,
                                 help_text="Don't send notifications for events below this level.")

class PushsaferNotifications(Plugin):

    author = 'Kevin Siml'
    author_url = 'https://www.pushsafer.com'
    title = 'Pushsafer'

    conf_title = 'Pushsafer'
    conf_key = 'pushsafer'

    resource_links = [
        ('Bug Tracker', 'https://github.com/appzer/sentry-pushsafer/issues'),
        ('Source', 'https://github.com/appzer/sentry-pushsafer'),
    ]

    version = sentry_pushsafer.VERSION
    project_conf_form = PushsaferSettingsForm

    def can_enable_for_projects(self):
        return True

    def is_setup(self, project):
        return all(self.get_option(key, project) for key in ('privatekey', 'device', 'icon', 'iconcolor', 'sound', 'vibration', 'time2live'))

    def post_process(self, group, event, is_new, is_sample, **kwargs):

        if not is_new or not self.is_setup(event.project):
            return

        if event.level < int(self.get_option('severity', event.project)):
            return

        title = '%s: %s' % (event.get_level_display().upper(), event.error().split('\n')[0])

        link = '%s/%s/group/%d/' % (settings.URL_PREFIX, group.project.slug, group.id)

        message = 'Server: %s\n' % event.server_name
        message += 'Group: %s\n' % event.group
        message += 'Logger: %s\n' % event.logger
        message += 'Message: %s\n' % event.message

        self.send_notification(title, message, link, event)

    def send_notification(self, title, message, link, event,):

        # see https://pushsafer.net/api

        params = {
            'k': self.get_option('privatekey', event.project),
            'd': self.get_option('device', event.project),
			'i': self.get_option('icon', event.project),
			'c': self.get_option('iconcolor', event.project),
			's': self.get_option('sound', event.project),
			'v': self.get_option('vibration', event.project),
			'l': self.get_option('time2live', event.project),
            'm': message,
            't': title,
            'u': link,
            'ut': 'More info',
            }
        requests.post('https://www.pushsafer.com/api', params=params)
