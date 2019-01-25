# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import biostar.apps.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='users.User')),
                ('energynote_email', models.CharField(null=True, default=None, max_length=255, blank=True, unique=True, verbose_name='Energy Note Email')),
                ('is_energynote_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('users.user',),
            managers=[
                ('objects', biostar.apps.users.models.LocalManager()),
            ],
        ),
        migrations.CreateModel(
            name='EnergyConsumption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField()),
                ('concept', models.CharField(max_length=50)),
                ('consumption', models.FloatField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='energyconsumption',
            unique_together=set([('email', 'timestamp', 'concept')]),
        ),
    ]
