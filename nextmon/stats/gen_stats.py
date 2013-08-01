#!/usr/bin/python
import os
import sys

if __name__ == '__main__':
    cur_file = os.path.abspath(__file__)
    django_dir = os.path.abspath(os.path.join(os.path.dirname(cur_file), '..'))
    sys.path.append(django_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import datetime

from django.db import transaction

import nextbus.models
import nextbus.api
import stats.models

if __name__ == '__main__':
    stats.models.DailySummary.populate()
