# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('context', models.CharField(default=b'', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(default=b'', max_length=200)),
                ('type', models.IntegerField(default=0, choices=[(0, b'Bronze'), (1, b'Silver'), (2, b'Gold')])),
                ('unique', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=0)),
                ('icon', models.CharField(default=b'fa fa-asterisk', max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='award',
            name='badge',
            field=models.ForeignKey(to='badges.Badge'),
        ),
    ]
