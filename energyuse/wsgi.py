"""
WSGI config for EnergyUse.
"""
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

#Env variables
os.environ['BIOSTAR_HOME']=BASE_DIR
os.environ['BIOSTAR_HOSTNAME']="energyuse.eu"
os.environ['BIOSTAR_ADMIN_NAME']="EnergyUse Community"
os.environ['BIOSTAR_ADMIN_EMAIL']="admin@energyuse.eu"
os.environ['DATABASE_NAME']="energyuse"
os.environ['SECRET_KEY']="a46c8dd4f89587580811b450c0d20004580fb595"
os.environ['DEFAULT_FROM_EMAIL']='noreply@energyuse.eu'

os.environ['EMAIL_BACKEND']='django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_SUBJECT_PREFIX']=''
os.environ['ACCOUNT_EMAIL_SUBJECT_PREFIX']=''
os.environ['ACCOUNT_EMAIL_SUBJECT_PREFIX']="[EnergyUse] "
os.environ['EMAIL_HOST']='localhost'
os.environ['EMAIL_PORT']='25'
os.environ['EMAIL_HOST_USER']=''
os.environ['EMAIL_HOST_PASSWORD']=''

#Settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energyuse.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
