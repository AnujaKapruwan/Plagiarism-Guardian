# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plag', '0009_auto_20140916_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='order',
        ),
    ]
