
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from energyuse import settings


class Record(models.Model):
    """
    Basic log record describing all user interaction with the UI.
    Will be propagated by a middle ware.
    This will be one BIG DB table!
    """
    created_at = models.DateTimeField(auto_now_add = True)
    sessionId = models.CharField(max_length=256)

    requestUser = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    requestPath  = models.TextField()
    requestQueryString = models.TextField()
    requestVars = models.TextField()
    requestMethod = models.CharField(max_length=4)
    requestSecure = models.BooleanField(default=False)
    requestAjax = models.BooleanField(default=False)
    #requestMETA = models.TextField(null=True, blank=True)
    requestAddress = models.GenericIPAddressField()

    viewFunction = models.CharField(max_length=256)
    viewDocString = models.TextField(null=True, blank=True)
    viewArgs = models.TextField()

    responseCode = models.CharField(max_length=3)

    def __unicode__(self):
        return self.viewFunction