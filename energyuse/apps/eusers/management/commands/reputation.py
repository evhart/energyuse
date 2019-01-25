from django.core.management.base import BaseCommand, CommandError
from biostar.apps.posts.models import Vote, Post
from energyuse.apps.eusers.models import User


class Command(BaseCommand):
    help = 'Recalculate user reputation'

    def handle(self, *args, **options):


        for user in User.objects.all():
            try:
                user.score = 0
                user.save()
            except:
                pass

        for post in Post.objects.all():
            try:
                post.author.score = post.author.score + post.score
                post.author.save()
            except:
                pass

        self.stdout.write('Done...')