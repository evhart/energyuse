# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default='')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('sent_at', models.DateTimeField(null=True, blank=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (2, 'Published')])),
            ],
        ),
        migrations.CreateModel(
            name='EmailSub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.IntegerField(choices=[(0, 'Subscribed'), (1, 'Unsubscribed')])),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('rank', models.FloatField(default=0, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(0, 'Pending'), (1, 'Open'), (2, 'Closed'), (3, 'Deleted')])),
                ('type', models.IntegerField(db_index=True, choices=[(0, 'Question'), (1, 'Answer'), (6, 'Comment'), (2, 'Job'), (3, 'Forum'), (8, 'Tutorial'), (7, 'Data'), (4, 'Page'), (10, 'Tool'), (11, 'News'), (5, 'Blog'), (9, 'Bulletin Board')])),
                ('vote_count', models.IntegerField(default=0, db_index=True, blank=True)),
                ('downvote_count', models.IntegerField(default=0, db_index=True, blank=True)),
                ('view_count', models.IntegerField(default=0, blank=True)),
                ('reply_count', models.IntegerField(default=0, blank=True)),
                ('comment_count', models.IntegerField(default=0, blank=True)),
                ('book_count', models.IntegerField(default=0)),
                ('changed', models.BooleanField(default=True)),
                ('subs_count', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0, db_index=True, blank=True)),
                ('thread_score', models.IntegerField(default=0, db_index=True, blank=True)),
                ('creation_date', models.DateTimeField(db_index=True)),
                ('lastedit_date', models.DateTimeField(db_index=True)),
                ('sticky', models.BooleanField(default=False, db_index=True)),
                ('has_accepted', models.BooleanField(default=False)),
                ('content', models.TextField(default='')),
                ('html', models.TextField(default='')),
                ('tag_val', models.CharField(default='', max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(default='', null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_created=True)),
                ('token', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, db_index=True, choices=[(3, b'default'), (0, b'local messages'), (1, b'email'), (4, b'email for every new thread (mailing list mode)')])),
                ('date', models.DateTimeField(verbose_name='Date', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, db_index=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(db_index=True, choices=[(0, 'Upvote'), (1, 'Downvote'), (2, 'Novote'), (3, 'Bookmark'), (4, 'Accept')])),
                ('date', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
    ]
