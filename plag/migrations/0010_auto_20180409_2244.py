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
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.DeleteModel(
            name='RecentBlogPosts',
        ),
        migrations.RemoveField(
            model_name='userpreference',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserPreference',
        ),
        migrations.RemoveField(
            model_name='protectedresource',
            name='next_scan',
        ),
        migrations.RemoveField(
            model_name='protectedresource',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.RemoveField(
            model_name='protectedresource',
            name='scan_frequency',
        ),
        migrations.AlterField(
            model_name='protectedresource',
            name='status',
            field=models.CharField(max_length=1, choices=[('A', 'Active'), ('S', 'Being scanned'), ('F', 'Last scan failed'), ('I', 'Inactive')], default='A'),
        ),
    ]
