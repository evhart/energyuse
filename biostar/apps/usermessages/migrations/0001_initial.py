# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, db_index=True, choices=[(3, b'default'), (0, b'local messages'), (1, b'email'), (4, b'email for every new thread (mailing list mode)')])),
                ('unread', models.BooleanField(default=True)),
                ('sent_at', models.DateTimeField(null=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageBody',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('subject', models.CharField(max_length=120, verbose_name='Subject')),
                ('sent_at', models.DateTimeField(verbose_name='sent at')),
            ],
        ),
    ]
