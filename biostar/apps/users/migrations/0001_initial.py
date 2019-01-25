# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import biostar.apps.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='Email', db_index=True)),
                ('type', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('date', models.DateTimeField(default=biostar.apps.users.models.now)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=255, db_index=True)),
                ('last_login', models.DateTimeField()),
                ('date_joined', models.DateTimeField()),
                ('location', models.CharField(default='', max_length=255, blank=True)),
                ('website', models.URLField(default='', max_length=255, blank=True)),
                ('scholar', models.CharField(default='', max_length=255, blank=True)),
                ('twitter_id', models.CharField(default='', max_length=255, blank=True)),
                ('my_tags', models.TextField(default='', max_length=255, blank=True)),
                ('info', models.TextField(default='', null=True, blank=True)),
                ('message_prefs', models.IntegerField(default=1, choices=[(3, b'default'), (0, b'local messages'), (1, b'email'), (4, b'email for every new thread (mailing list mode)')])),
                ('flag', models.IntegerField(default=0)),
                ('watched_tags', models.CharField(default='', max_length=100, blank=True)),
                ('digest_prefs', models.IntegerField(default=2, choices=[(0, 'Never'), (1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')])),
                ('opt_in', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='Email', db_index=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('type', models.IntegerField(default=0, choices=[(0, 'User'), (1, 'Moderator'), (2, 'Admin'), (3, 'Blog')])),
                ('status', models.IntegerField(default=0, choices=[(0, 'New User'), (1, 'Trusted'), (2, 'Suspended'), (3, 'Banned')])),
                ('new_messages', models.IntegerField(default=0)),
                ('badges', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('activity', models.IntegerField(default=0)),
                ('flair', models.CharField(default='', max_length=15, verbose_name='Flair')),
                ('site', models.ForeignKey(to='sites.Site', null=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', biostar.apps.users.models.LocalManager()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='tags',
            field=models.ManyToManyField(to='users.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to='users.User'),
        ),
    ]
