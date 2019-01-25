
from django.http import HttpResponse, HttpResponseNotFound
from biostar.apps.posts.models import Tag
from biostar.apps.users.models import Profile
from django.shortcuts import redirect
from energyuse.eserver import views as eviews
from django.contrib import messages

def subscribe(request,topic):
    context = {}
    if request.user.is_authenticated():
            context['is_subscribed'] = Profile.objects.filter(user=request.user, tags__name=topic).exists()
            if context['is_subscribed']:
                profile = Profile.objects.get(user=request.user)
                profile.add_tags(profile.watched_tags.replace(', ' + topic, ''))
                profile.save()


                messages.info(request, "You are now unfollowing: <code>%s</code>." % topic)
            else:
                profile = Profile.objects.get(user=request.user)
                profile.add_tags(profile.watched_tags + ', ' + topic)
                profile.save()

                messages.info(request, "You are now following: <code>%s</code>." % topic)


    return redirect("topic-list", topic=topic)

