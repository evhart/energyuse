# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name=b'Blog Name')),
                ('desc', models.TextField(default=b'', blank=True)),
                ('feed', models.URLField()),
                ('link', models.URLField()),
                ('active', models.BooleanField(default=True)),
                ('list_order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(default=b'', max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(default=b'', max_length=20000)),
                ('html', models.TextField(default=b'')),
                ('creation_date', models.DateTimeField(db_index=True)),
                ('insert_date', models.DateTimeField(null=True, db_index=True)),
                ('published', models.BooleanField(default=False)),
                ('link', models.URLField()),
                ('blog', models.ForeignKey(to='planet.Blog')),
            ],
        ),
    ]
