from __future__ import print_function, unicode_literals, absolute_import, division
import logging

import biostar
from biostar.apps.users.models import LocalManager, Profile, NEW_USER_WELCOME_TEMPLATE
from biostar.apps import util
from django.db import models


logger = logging.getLogger(__name__)


class User(biostar.apps.users.models.User):
    objects = LocalManager()

    energynote_email = models.CharField(verbose_name='Energy Note Email', max_length=255, unique=True, blank=True, null=True, default=None)
    is_energynote_verified = models.BooleanField(default=False)

    #@property
    def is_superuser(self):
        return self.is_admin

    #@property
    def is_staff(self):
        return self.is_admin



from django.db.models.signals import post_save
post_save.connect(Profile.auto_create, sender=User)



def user_create_messages(sender, instance, created, *args, **kwargs):
    "The actions to undertake when creating a new post"
    from biostar.apps.usermessages.models import Message, MessageBody
    from biostar.apps.util import html
    from biostar.const import now

    user = instance
    if created:
        # Create a welcome message to a user
        # We do this so that tests pass, there is no admin user there
        authors = User.objects.filter(is_admin=True) or [user]
        author = authors[0]

        title = "Welcome!"
        content = html.render(name=NEW_USER_WELCOME_TEMPLATE, user=user)
        body = MessageBody.objects.create(author=author, subject=title,
                                          text=content, sent_at=now())
        message = Message(user=user, body=body, sent_at=body.sent_at)
        message.save()

# Creates a message to everyone involved
post_save.connect(user_create_messages, sender=User, dispatch_uid="user-create_messages")




class EnergyConsumption(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField()
    concept = models.CharField(max_length=50)
    consumption = models.FloatField()

    class Meta:
        unique_together = (("email", "timestamp", "concept"),)

    @staticmethod
    def average_consumption(email, concept='all'):
        avgenergy = EnergyConsumption.objects.filter(email=email, concept=concept).extra(select={'day': 'date( timestamp )'}).values('day').annotate(total=Sum('consumption'))
        if len(avgenergy) > 0:
              avgenergy = reduce(lambda x, y: x + y, map(lambda x: x['total'], avgenergy)) / len(avgenergy)
        else:
              avgenergy = None
        return avgenergy

