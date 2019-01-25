from django import template
from energyuse.apps.eusers.models import EnergyConsumption

register = template.Library()

@register.assignment_tag
def average_consumption(email,concept='all'):
    return EnergyConsumption.average_consumption(email, concept)
