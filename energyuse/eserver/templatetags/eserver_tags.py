from django import forms
from django import template
from django.conf import settings
from django.template import Context, Template
from django.template.defaultfilters import stringfilter
from django.core.context_processors import csrf
from biostar.apps.posts.models import Post, Tag
from biostar.apps.usermessages.models import Message
import random, hashlib, urllib
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django import template
from django.core.urlresolvers import reverse
from biostar import const
from biostar.server.views import LATEST
from energyuse.apps.concepts.models import Concept
from energyuse.apps.consumption.forms import ManualEnergyConsumptionForm
from energyuse.apps.consumption.models import ManualEnergyConsumption
from energyuse.apps.eusers.models import User, EnergyConsumption
from django.db.models import Sum

register = template.Library()


@register.inclusion_tag('server_tags/page_featured.html')
def featured():
    "Renders a list of featured posts"
    posts = Post.objects.all().order_by('-book_count')[:5]
    return {'featured_posts': posts}
    # marker = "&bull;"
    # if user.is_admin:
    #     marker = '&diams;&diams;'
    # elif user.is_moderator:
    #     marker = '&diams;'
    # return {'user': user, 'marker': marker}


@register.inclusion_tag('server_tags/page_top_contributors.html')
def top_contributors():
    "Renders a list of top users"
    users = User.objects.all().order_by('-score')[:3]
    return {'top_users': users}
    # marker = "&bull;"
    # if user.is_admin:
    #     marker = '&diams;&diams;'
    # elif user.is_moderator:
    #     marker = '&diams;'
    # return {'user': user, 'marker': marker}



@register.inclusion_tag('server_tags/page_featured_tags.html')
def featured_tags():
    "Renders a list of top tags that have description and icons"

    concepts = Concept.objects.exclude(icon__isnull=True, fullname='', description='').order_by('-tag__count').distinct()[:4]
    # for c in concepts:
    #     print c.fullname
    return {'top_topics': concepts}


@register.inclusion_tag('server_tags/block_consumption.html', takes_context=True)
def average_consumption(context):
    print(context)

    user_avgenergy = -1 #no account
    if context['request'].user.is_authenticated():
        current_user = context['request'].user
        #euser = User.objects.get(user=current_user)
        euser = current_user

        if euser.is_energynote_verified:
            user_avgenergy = EnergyConsumption.objects.filter(email=euser.energynote_email, concept="all").extra(select={'day': 'date( timestamp )'}).values('day').annotate(total=Sum('consumption'))
            if len(user_avgenergy) > 0:
                user_avgenergy = reduce(lambda x, y: x + y, map(lambda x: x['total'], user_avgenergy)) / len(user_avgenergy)
            else:
                user_avgenergy = -2 #account no data

    community_avgenergy = -1
    community_avgenergy = EnergyConsumption.objects.filter(email=0, concept="all").extra(select={'day': 'date( timestamp )'}).values('day').annotate(total=Sum('consumption'))
    if len(community_avgenergy) > 0:
        community_avgenergy = reduce(lambda x, y: x + y, map(lambda x: x['total'], community_avgenergy)) / len(community_avgenergy)
    else:
        community_avgenergy = -2 #account no data

    return {
            "user_avgenergy": round(user_avgenergy, 4),
            "community_avgenergy": round(community_avgenergy, 4)
    }


@register.inclusion_tag('server_tags/block_tag_consumption.html', takes_context=True)
def average_tag_consumption(context,tag):
    print(context)


    #TODO Integrate averages
    user_avgenergy = -1 #no account
    if context['request'].user.is_authenticated():
        current_user = context['request'].user
        #euser = User.objects.get(user=current_user)
        euser = current_user

        if euser.is_energynote_verified:
            user_avgenergy = EnergyConsumption.objects.filter(email=euser.energynote_email, concept=tag.tag.name).extra(select={'day': 'date( timestamp )'}).values('day').annotate(total=Sum('consumption'))
            if len(user_avgenergy) > 0:
                user_avgenergy = reduce(lambda x, y: x + y, map(lambda x: x['total'], user_avgenergy)) / len(user_avgenergy)
            else:
                user_avgenergy = -2 #account no data



    #########################################
    community_avgenergy = -1


    #community_submitted = ManualEnergyConsumption.objects.filter(concept=tag.tag.name) #Select
    community_avgenergy = EnergyConsumption.objects.filter(email=0, concept=tag.tag.name).extra(select={'day': 'date( timestamp )'}).values('day').annotate(total=Sum('consumption'))

    if len(community_avgenergy) > 0:
        community_avgenergy = reduce(lambda x, y: x + y, map(lambda x: x['total'], community_avgenergy)) / len(community_avgenergy)
    else:
        community_avgenergy = -2 #account no data


    #########################################

    return {
            "user_avgenergy": round(user_avgenergy, 4),
            "community_avgenergy": round(community_avgenergy, 4)
    }


@register.inclusion_tag('server_tags/block_tag_submitconsumption.html', takes_context=True)
def submit_tag_consumption(context,tag):

    request = context['request'].method
    form = ManualEnergyConsumptionForm(initial={'concept': tag})

    # if context['request'].method == 'POST':
    #     print "dsadasdsadda"
    #
    #     if context['request'].user.is_authenticated:
    #
    #         form = form(request.POST, user=request.user)
    #         if form.is_valid():
    #             f = form.cleaned_data
    #             consumption = ManualEnergyConsumption(concept=f['concept'], consumption=f['consumption'], user=request.user)
    #             consumption.save()
    #
    #             #messages.success(request, "Reading added successfully")
    #
    # else:
    context2 = context
    context2['concept'] = tag

    form.fields['concept'].widget = forms.HiddenInput()
    context['form'] = form

    return context