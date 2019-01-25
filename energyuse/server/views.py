import logging
import biostar


from biostar.apps.users import auth
from biostar.apps.users.models import Profile
from biostar.server.views import BaseListMixin, AUTH_TOPIC, reset_counts, LATEST, posts_by_topic, apply_sort, MYPOSTS, \
    MYTAGS, UNANSWERED, FOLLOWING, BOOKMARKS, POST_TYPES
from energyuse import settings
from energyuse.apps.concepts.models import Concept
from energyuse.apps.eusers.models import User
from energyuse.apps.eusers.views import EditUser, EditEnergyNote

from biostar.apps.posts.models import Post, Tag
from biostar.apps.badges.models import Award
from django.contrib import messages
from biostar import const
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)




class UserDetails(biostar.server.views.UserDetails):
    """
    Renders a user profile.
    """
    model = User
    template_name = "user_details.html"
    context_object_name = "target"


class EditUser(EditUser):
    template_name = "user_edit.html"



class EditEnergyNote(EditEnergyNote):
    template_name = "energynote_edit.html"




def posts_by_topic(request, topic):
    "Returns a post query that matches a topic"
    user = request.user

    # One letter tags are always uppercase
    topic = Tag.fixcase(topic)

    if topic == MYPOSTS:
        # Get the posts that the user wrote.
        return Post.objects.my_posts(target=user, user=user)

    if topic == MYTAGS:
        # Get the posts that the user wrote.
        messages.success(request,
                         'Posts matching the <b><i class="fa fa-tag"></i> My Tags</b> setting in your user profile')
        return Post.objects.tag_search(user.profile.my_tags)

    if topic == UNANSWERED:
        # Get unanswered posts.
        return Post.objects.top_level(user).filter(type=Post.QUESTION, reply_count=0)

    if topic == FOLLOWING:
        # Get that posts that a user follows.
        messages.success(request, 'Threads that will produce notifications.')
        return Post.objects.top_level(user).filter(subs__user=user)

    if topic == BOOKMARKS:
        # Get that posts that a user bookmarked.
        return Post.objects.my_bookmarks(user)

    if topic in POST_TYPES:
        # A post type.
        return Post.objects.top_level(user).filter(type=POST_TYPES[topic])

    if topic and topic != LATEST:
        # Any type of topic.
        #if topic:
            #messages.info(request,
            #             "Showing: <code>%s</code> &bull; <a href='/'>reset</a>" % topic)
        return Post.objects.tag_search(topic)

    # Return latest by default.
    return Post.objects.top_level(user)


class TagPage(BaseListMixin):
    """
    This is the base class for any view that produces a list of posts.
    """
    model = Post
    template_name = "tag_page.html"
    context_object_name = "posts"
    paginate_by = settings.PAGINATE_BY
    LATEST = "Latest"

    def __init__(self, *args, **kwds):
        super(TagPage, self).__init__(*args, **kwds)
        self.limit = 250
        self.topic = None

    def get_title(self):
        if self.topic:
            return "%s Posts" % self.topic
        else:
            return "Latest Posts"

    def get_queryset(self):
        self.topic = self.kwargs.get("topic", "")

        # Catch expired sessions accessing user related information
        if self.topic in AUTH_TOPIC and self.request.user.is_anonymous():
            messages.warning(self.request, "Session expired")
            self.topic = LATEST

        query = posts_by_topic(self.request, self.topic)
        query = apply_sort(self.request, query)

        # Limit latest topics to a few pages.
        if not self.topic:
            query = query[:settings.SITE_LATEST_POST_LIMIT]
        return query

    def get_context_data(self, **kwargs):
        session = self.request.session

        context = super(TagPage, self).get_context_data(**kwargs)
        context['topic'] = self.topic or self.LATEST

        try:
            context['tag'] = Concept.objects.get(tag__name=context['topic'])
        except Concept.DoesNotExist:
            context['tag'] = None

        reset_counts(self.request, self.topic)


        #Get info about tag subsciptions:
        context['nb_sub'] = Profile.objects.filter(tags__name=context['topic']).count()
        if self.request.user.is_authenticated():
            context['is_subscribed'] = Profile.objects.filter(user=self.request.user, tags__name=context['topic']).exists()
        else:
            context['is_subscribed'] = False

        return context

