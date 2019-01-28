from os.path import join
from biostar.settings.base import *
import MySQLdb

SITE_ID = 1

# The start categories. These tags have special meaning internally.
START_CATEGORIES = []
    # "Latest", "Tutorials", "Tools",  "Jobs", "Forum", "Unanswered",
# ]

# These should be the most frequent (or special) tags on the site.
# NAVBAR_TAGS = [
#     "Test1", "Test2",
# ]

NAVBAR_TAGS = []

# The last categories. Right now are empty.
END_CATEGORIES = [

]

END_CATEGORIES = []

# These are the tags that will show up in the tag recommendation dropdown.
POST_TAG_LIST = NAVBAR_TAGS

# This will form the navbar
CATEGORIES = [] #START_CATEGORIES + NAVBAR_TAGS + END_CATEGORIES

#########################################################################
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    # Django specific context processors.
    "django.core.context_processors.debug",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",

    # Social authorization specific context.
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",

    # Biostar specific context.
    'biostar.server.context.shortcuts',
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'energyuse',  'eserver',  'templates'),
    TEMPLATE_DIR,
)


STATICFILES_DIRS = (
    os.path.join(BASE_DIR,  'energyuse',    'static'),
    STATIC_DIR,
)

DATABASES = {
    'default':
        {'ENGINE': 'django.db.backends.mysql',
         'NAME': 'energyuse',
         'HOST': '127.0.0.1',
         'USER': 'energyuse',
         'PASSWORD': 'wG4bbnKSV7Y4ue9d',
         'PORT': '3306',

         }
}


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',


    # 'django.contrib.sessions',

    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # The javascript and CSS asset manager.
    'compressor',

    # Enabling the admin and its documentation.
    'grappelli',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.sessions',

    # Biostar specific apps.
    'biostar.apps.users',
    'biostar.apps.util',
    'biostar.apps.posts',
    'biostar.apps.usermessages',
    'biostar.apps.badges',
    'biostar.apps.planet',

    # The main Biostar server.
    'biostar.server',


    #Energyuse specific apps.
    'energyuse.apps.concepts',
    'energyuse.apps.eusers',
    'energyuse.eserver',

    # Social login handlers.
    'allauth',
    'allauth.account',
    #'allauth.socialaccount',
    #'allauth.socialaccount.providers.persona',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.orcid',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.weibo',

    # External apps.
    'haystack',
    'crispy_forms',
    'djcelery',
    'kombu.transport.django',
    #'south',
    'captcha',

    'easy_thumbnails',
    'filer',
    'mptt',
    'inplaceeditform',
    'inplaceeditform_extra_fields',
    'cookielaw',
    'energyuse.apps.logall',
]


SOCIALACCOUNT_PROVIDERS = {

    #'facebook': {
    #    'SCOPE': ['email'],
    #    'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    #    'METHOD': 'oauth2',
    #    'LOCALE_FUNC': lambda x: 'en_US',
    #    'PROVIDER_KEY': get_env("FACEBOOK_PROVIDER_KEY"),
    #    'PROVIDER_SECRET_KEY': get_env("FACEBOOK_PROVIDER_SECRET_KEY"),
    #},
    #
    # 'persona': {
    #     'REQUEST_PARAMETERS': {'siteName': 'Biostar'}
    # },
    #
    # 'github': {
    #     'SCOPE': ['email'],
    #     'PROVIDER_KEY': get_env("GITHUB_PROVIDER_KEY"),
    #     'PROVIDER_SECRET_KEY': get_env("GITHUB_PROVIDER_SECRET_KEY"),
    # },
    #
    # 'google': {
    #     'SCOPE': ['email', 'https://www.googleapis.com/auth/userinfo.profile'],
    #     'AUTH_PARAMS': {'access_type': 'online'},
    #     'PROVIDER_KEY': get_env("GOOGLE_PROVIDER_KEY"),
    #     'PROVIDER_SECRET_KEY': get_env("GOOGLE_PROVIDER_SECRET_KEY"),
    # },

    #'orcid': {
    #    'PROVIDER_KEY': get_env("ORCID_PROVIDER_KEY"),
    #    'PROVIDER_SECRET_KEY': get_env("ORCID_PROVIDER_SECRET_KEY"),
    #},
}


# The celery configuration file
CELERY_CONFIG = 'biostar.celeryconfig'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

AUTH_USER_MODEL = 'eusers.User'

ROOT_URLCONF = 'energyuse.urls'

# ACCOUNT_SIGNUP_FORM_CLASS = 'energyuse.apps.eusers.forms.SignupForm'

# ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USERNAME_REQUIRED = True

# ACCOUNT_FORMS = {'login': 'energyuse.apps.eusers.forms.LoginForm'}

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'name'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

ADAPTOR_INPLACEEDIT = {'auto_fk': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteForeingKeyField',
                       'auto_m2m': 'inplaceeditform_extra_fields.fields.AdaptorAutoCompleteManyToManyField',
                       'image_thumb': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
                       'tiny': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',
                       'tiny_simple': 'inplaceeditform_extra_fields.fields.AdaptorSimpleTinyMCEField'}


# FILEBROWSER_DIRECTORY = os.path.join(BASE_DIR, '/media/')
THUMBNAIL_HIGH_RESOLUTION = True


GOOGLE_TRACKER='UA-71076885-1'
GOOGLE_DOMAIN=''

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'biostar.server.middleware.Visit',
    'energyuse.apps.logall.middleware.LogAllMiddleware',
)

DEFAULT_MESSAGE_PREF = "email"

MEDIA_ROOT=os.path.join(BASE_DIR, 'live', 'export', 'media').replace('\\', '/') #'live/export/media'
MEDIA_URL='/media/'





# DEBUG = False
# DEFAULT_FROM_EMAIL='Energyuse.eu <noreply@energyuse.eu>'
DEFAULT_FROM_EMAIL='noreply@energyuse.eu'
# EMAIL_PORT = 465
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'smtp.zoho.com'
# EMAIL_HOST_USER = 'web@energyuse.eu'
# EMAIL_HOST_PASSWORD = 'nNNx7Qk5znUazZhM'
EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[EnergyUse] '


EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

#What domain will handle the replies.
EMAIL_REPLY_PATTERN = "reply+%s+code@energyuse.eu"

# The format of the email that is sent
EMAIL_FROM_PATTERN = u'''"%s on EnergyUse" <%s>'''

# The secret key that is required to parse the email
EMAIL_REPLY_SECRET_KEY = "abc"


# The subject of the reply goes here
EMAIL_REPLY_SUBJECT = u"[EnergyUse] %s"

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} > {outfile}'),
)

ALLOWED_HOSTS = ['*']
DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True


SERVE_MEDIA=True