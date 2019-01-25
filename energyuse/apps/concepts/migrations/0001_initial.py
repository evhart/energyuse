# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullname', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('appliance', models.BooleanField(default=False)),
                ('image_source', models.CharField(max_length=50, null=True, blank=True)),
                ('image_author', models.CharField(max_length=50, null=True, blank=True)),
                ('generated', models.BooleanField(default=False)),
                ('linked_concept', models.URLField(null=True, blank=True)),
                ('icon', filer.fields.image.FilerImageField(related_name='concept_icon', blank=True, to='filer.Image', null=True)),
                ('image', filer.fields.image.FilerImageField(related_name='concept_image', blank=True, to='filer.Image', null=True)),
            ],
        ),
    ]
