import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
sys.path.insert(1,'/data/web/energyuse.eu/energyuse')
sys.path.insert(1,'/data/web/energyuse.eu/energyuse/mailling/')
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
import csv
import operator


messages = []
#users = [{'firstname': 'abc', 'email': "gregoire.burel@gmail.com"}]
with open('./mails/participants.csv','rU') as csvfile:
    users = csv.DictReader(csvfile)

    for user in users:
        #print(user)
        msg_plain = render_to_string('announcement3.txt', {'username': user['firstname']})
        #print(msg_plain)
        messages.append(('News from EnergyUse', msg_plain, 'Energyuse.eu <contact@energyuse.eu>', [user['email']]))
    print messages
    send_mass_mail(list(messages), fail_silently=False)