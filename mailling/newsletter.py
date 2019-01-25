import os
import sys
sys.path.insert(1,'/Users/gb6366/git/decarbonet/django_site/')
sys.path.insert(1,'/Users/gb6366/git/decarbonet/mailling/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms_site.settings")


import django
import cms_site.settings
cms_site.settings.TEMPLATE_DIRS = (os.path.join(cms_site.settings.BASE_DIR, '..', 'mailling', 'templates'),)

django.setup()

from datetime import datetime, timedelta
last_month = datetime.today() - timedelta(days=45)


from decarbonet_user.models import DecarbonetUser, UserMessage
from django.contrib.auth.models import User
from hints.models import Hint
from django.contrib.comments import Comment
from updown.models import Vote
from concepts.models import Concept
from sets import Set
from django.db.models import Count, Sum
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail, send_mail
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict
import csv
import operator

nbusers =  User.objects.filter(date_joined__gte=last_month).count()
nbposts = Hint.objects.filter(date_created__gte=last_month).count()
nbcomments = Comment.objects.filter(submit_date__gte=last_month).count()
nbvotes = Vote.objects.filter(date_added__gte=last_month).count()

#print(nbusers, nbposts,nbcomments,nbvotes)

#Get the last 5 posts, then get the associated tags
#lastTags = Concept.objects.count()
latestHints = Hint.objects.order_by('-date_created')[:5]
lastTags = Set([])
for hint in latestHints:
    print(hint.concepts.all())
    lastTags = lastTags | Set(hint.concepts.all())

#user.comment_comments.all().count()
topContributors = []
for user in User.objects.annotate(post_count=Count('hint'),comment_count=Count('comment_comments')):
    if not u"decarbonet" in user.username:
        topContributors.append((user,user.post_count + user.comment_count))
topContributors.sort(key=lambda x: x[1], reverse=True)

#print(lastTags, topContributors[:3])
topContributors = map(lambda x: x[0], topContributors)


#top tag:
topTag = defaultdict(lambda: 0)
for hint in Hint.objects.filter(date_created__gte=last_month):
    #Get the number of comments:
    ct = ContentType.objects.get_for_model(Hint)
    obj_pk = hint.id
    nbcomments = Comment.objects.filter(content_type=ct,object_pk=obj_pk).count()

    #Update the number of tags:
    for concept in hint.concepts.all():
        topTag[concept.name] += nbcomments + 1

print(topTag)
print(max(topTag.iteritems(), key=operator.itemgetter(1))[0])
topTag = max(topTag.iteritems(), key=operator.itemgetter(1))[0]



messages = []
#users = [{'firstname': 'abc', 'email': "gregoire.burel@gmail.com"}]
with open('./mails/participantstest.csv','rU') as csvfile:
    users = csv.DictReader(csvfile)

    for user in users:
        #print(user)
        msg_plain = render_to_string('newsletter.txt', {'username': user['firstname'], 'lastTags': list(lastTags)[:5], 'topContributors': topContributors[:3], 'nbusers': nbusers, 'nbposts': nbposts + nbcomments, 'nbvotes': nbvotes, 'topTag': topTag})
        #print(msg_plain)
        messages.append(('News from EnergyUse', msg_plain, 'Energyuse.eu <contact@energyuse.eu>', [user['email']]))
    print messages
    #send_mass_mail(list(messages), fail_silently=False)

