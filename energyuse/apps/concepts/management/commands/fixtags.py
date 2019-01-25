from django.core.management.base import BaseCommand, CommandError
import json
import re
import urllib
from biostar.apps.posts.models import Vote, Post, Tag
from energyuse.apps.concepts.models import Concept
from energyuse.apps.eusers.models import User


class Command(BaseCommand):
    help = 'Fix missing tags from field'

    def handle(self, *args, **options):

         for post in Post.objects.filter(type__in=Post.TOP_LEVEL):
            try:
               tags = ",".join(map(lambda x: x.name, post.tag_set.all()))
               post.add_tags(tags)
               post.tag_val = tags
               post.save()



            except:
                pass

         self.stdout.write('Done...')
