# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plag', '0010_auto_20180409_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protectedresource',
            name='status',
        ),
    ]
