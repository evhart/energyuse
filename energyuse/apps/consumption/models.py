from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import mail
import logging

from energyuse.apps.concepts.models import Concept

logger = logging.getLogger(__name__)



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


class ManualEnergyConsumption(models.Model):
    class Meta:
        unique_together = (("user", "creation_date", "concept"),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_date = models.DateTimeField(auto_now_add=True, db_index=True)
    concept = models.ForeignKey(Concept, db_index=True)
    consumption = models.FloatField()


#class ConsumptionStatistics:
#