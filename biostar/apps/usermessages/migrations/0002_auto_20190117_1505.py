# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usermessages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='messagebody',
            name='author',
            field=models.ForeignKey(related_name='sent_messages', verbose_name='Sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messagebody',
            name='parent_msg',
            field=models.ForeignKey(related_name='next_messages', verbose_name='Parent message', blank=True, to='usermessages.MessageBody', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='body',
            field=models.ForeignKey(related_name='messages', verbose_name='Message', to='usermessages.MessageBody'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(related_name='recipients', verbose_name='Recipient', to=settings.AUTH_USER_MODEL),
        ),
    ]
