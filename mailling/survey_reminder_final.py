# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(1,'/data/web/energyuse.eu/energyuse2')
sys.path.insert(1,'/data/web/energyuse.eu/energyuse2/mailling/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energyuse.settings")


import django
import energyuse.settings
energyuse.settings.TEMPLATE_DIRS = (os.path.join(energyuse.settings.BASE_DIR, 'mailling', 'templates'),)

print energyuse.settings.TEMPLATE_DIRS

django.setup()

from datetime import datetime, timedelta
last_month = datetime.today() - timedelta(days=45)

from sets import Set
from django.db.models import Count, Sum
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail, send_mail
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict
from django.db import models

import csv
import operator

from django.contrib.auth import get_user_model
User = get_user_model()

# users = User.objects.all()
# for user in users:
#     print {name,user.email

replied = []
messages = []
#users = [{'firstname': 'abc', 'email': "gregoire.burel@gmail.com"}]
with open('./mails/participants.csv','rU') as csvfile:
   users_dic = csv.DictReader(csvfile)
   users = [user for user in users_dic]
    
   emails = [user['email'] for user in users]
   
    
   users2 = []
   for user in User.objects.all():
       if user.email not in emails:
            users2.append({"username": user.name.title(), "email": user.email})
        
   for user in users:
       if user['email'] not in replied:
            #print(user)
            msg_plain = render_to_string('survey3.txt', {'username': user['firstname']})
            #print(msg_plain)
            messages.append(('Final Reminder: Your feedback for the Energy Trial is really important to us.', msg_plain, 'Energyuse.eu <contact@energyuse.eu>', [user['email']]))
    
   print len(messages)
   
   for user in users2:
        #print(user)
        if user['email'] not in replied:
            msg_plain = render_to_string('survey3.txt', {'username': user['username']})
            #print(msg_plain)
            messages.append(('Final Reminder: Your feedback for the Energy Trial is really important to us.', msg_plain, 'Energyuse.eu <contact@energyuse.eu>', [user['email']]))



print messages[1]
print len(messages)
