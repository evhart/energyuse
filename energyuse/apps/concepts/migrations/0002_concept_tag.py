# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        ('concepts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='concept',
            name='tag',
            field=models.OneToOneField(null=True, blank=True, to='posts.Tag'),
        ),
    ]
