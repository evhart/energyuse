# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sessionId', models.CharField(max_length=256)),
                ('requestPath', models.TextField()),
                ('requestQueryString', models.TextField()),
                ('requestVars', models.TextField()),
                ('requestMethod', models.CharField(max_length=4)),
                ('requestSecure', models.BooleanField(default=False)),
                ('requestAjax', models.BooleanField(default=False)),
                ('requestAddress', models.GenericIPAddressField()),
                ('viewFunction', models.CharField(max_length=256)),
                ('viewDocString', models.TextField(null=True, blank=True)),
                ('viewArgs', models.TextField()),
                ('responseCode', models.CharField(max_length=3)),
            ],
        ),
    ]
