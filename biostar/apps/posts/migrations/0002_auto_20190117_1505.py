# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vote',
            name='post',
            field=models.ForeignKey(related_name='votes', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='post',
            field=models.ForeignKey(related_name='subs', verbose_name='Post', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='replytoken',
            name='post',
            field=models.ForeignKey(to='posts.Post'),
        ),
        migrations.AddField(
            model_name='replytoken',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postview',
            name='post',
            field=models.ForeignKey(related_name='post_views', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='lastedit_user',
            field=models.ForeignKey(related_name='editor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='posts.Post', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='root',
            field=models.ForeignKey(related_name='descendants', blank=True, to='posts.Post', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='site',
            field=models.ForeignKey(to='sites.Site', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='tag_set',
            field=models.ManyToManyField(to='posts.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='emailentry',
            name='post',
            field=models.ForeignKey(to='posts.Post', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('user', 'post')]),
        ),
    ]
