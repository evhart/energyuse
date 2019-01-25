import csv
import logging
import biostar
from biostar.apps.posts.auth import post_permissions

from biostar.apps.users import auth
from biostar.apps.users.models import Profile
from biostar.server.views import BaseListMixin, AUTH_TOPIC, reset_counts, LATEST, posts_by_topic, apply_sort, MYPOSTS, \
    MYTAGS, UNANSWERED, FOLLOWING, BOOKMARKS, POST_TYPES
from energyuse import settings
from energyuse.apps.concepts.models import Concept
from energyuse.apps.eusers.models import User, EnergyConsumption
from energyuse.apps.eusers.views import EditUser, EditEnergyNote

from biostar.apps.posts.models import Post, Tag, Subscription, Vote
from biostar.apps.badges.models import Award
from django.contrib import messages
from biostar import const
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import Http404
from rdflib import Graph, plugin
from rdflib.serializer import Serializer
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF, RDF
from django.db.models import Sum
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, View
from django.http import HttpResponseRedirect
from biostar.const import OrderedDict
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)




class UserDetails(biostar.server.views.UserDetails):
    """
    Renders a user profile.
    """
    model = User
    template_name = "user_details.html"
    context_object_name = "target"


    def get_context_data(self, **kwargs):
        context = super(UserDetails, self).get_context_data(**kwargs)
        target = context[self.context_object_name]
        #posts = Post.objects.filter(author=target).defer("content").order_by("-creation_date")
        posts = Post.objects.my_posts(target=target, user=self.request.user)
        paginator = Paginator(posts, 10)
        try:
            page = int(self.request.GET.get("page", 1))
            page_obj = paginator.page(page)
        except Exception, exc:
            messages.error(self.request, "Invalid page number")
            page_obj = paginator.page(1)
        context['page_obj'] = page_obj
        context['posts'] = page_obj.object_list
        awards = Award.objects.filter(user=target).select_related("badge", "user").order_by("-date")
        context['awards'] = awards[:25]



        #Get RDF content:
        EU = Namespace("http://socsem.open.ac.uk/ontologies/eu#")
        node = URIRef(self.request.build_absolute_uri())
        g = Graph()
        g.add( (node, RDF.type, EU.UserAccount) )
        g.add( (node, EU.username, Literal(target.name)) )
        g.add( (node, EU.reputation, Literal(target.score)) )
        context['json_ld'] = g.serialize(format='json-ld', indent=4)



        # Get user's ORCID profile URL.
        try:
            social_account = target.socialaccount_set.get(provider__icontains='orcid')
            context['orcid_profile_url'] = (social_account.extra_data['orcid-profile']
                                            ['orcid-identifier']['uri'])
            context['orcid_id'] = (social_account.extra_data['orcid-profile']
                                            ['orcid-identifier']['path'])
        except Exception:
            pass


        return context

#
# class UserConsumptionDetails(biostar.server.views.UserDetails):
#     """
#     Renders a user consumption.
#     """
#     model = User
#     template_name = "user_details.html"
#     context_object_name = "target"
#
#
#     def get_object(self):
#         obj = super(UserDetails, self).get_object()
#         obj = auth.user_permissions(request=self.request, target=obj)
#         return obj
#
#     def get_context_data(self, **kwargs):
#         context = super(UserDetails, self).get_context_data(**kwargs)
#         target = context[self.context_object_name]
#         #posts = Post.objects.filter(author=target).defer("content").order_by("-creation_date")
#         posts = Post.objects.my_posts(target=target, user=self.request.user)
#         paginator = Paginator(posts, 10)
#         try:
#             page = int(self.request.GET.get("page", 1))
#             page_obj = paginator.page(page)
#         except Exception, exc:
#             messages.error(self.request, "Invalid page number")
#             page_obj = paginator.page(1)
#         context['page_obj'] = page_obj
#         context['posts'] = page_obj.object_list
#         awards = Award.objects.filter(user=target).select_related("badge", "user").order_by("-date")
#         context['awards'] = awards[:25]
#
#         # Get user's ORCID profile URL.
#         try:
#             social_account = target.socialaccount_set.get(provider__icontains='orcid')
#             context['orcid_profile_url'] = (social_account.extra_data['orcid-profile']
#                                             ['orcid-identifier']['uri'])
#             context['orcid_id'] = (social_account.extra_data['orcid-profile']
#                                             ['orcid-identifier']['path'])
#         except Exception:
#             pass
#
#         return context



    def data(request, slug):
        try:
            user = User.objects.get(username=slug)
            decarb_user = DecarbonetUser.objects.get(user_id=user.id)

            if decarb_user.energyNoteVerified is False:
                raise Http404("User does not have any data")

        except DecarbonetUser.DoesNotExist:
            raise Http404("User does not exist")

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="consumption.csv"'

        writer = csv.writer(response)

        consumption_set = EnergyConsumption.objects.filter(email=decarb_user.energyNoteEmail)
        writer.writerow(['t', 'concept', 'consumption'])
        for consumption in consumption_set:
            writer.writerow([consumption.timestamp, consumption.concept, consumption.consumption])

        return response




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

        #print(context['topic'])
        if context['topic']:
            # Get RDF content:
            concept = Concept.objects.get(tag__name=context['topic'])
            EU = Namespace("http://socsem.open.ac.uk/ontologies/eu#")
            node = URIRef(self.request.build_absolute_uri())
            g = Graph()

            if concept.appliance:
                g.add((node, RDF.type, EU.Appliance))

                #Check if we have some consumption data:


                community_avgenergy = EnergyConsumption.objects.filter(email=0, concept=context['topic']).extra(
                    select={'day': 'date( timestamp )'}).values('day').annotate(total=Sum('consumption'))
                nb_obs = len(community_avgenergy)

                if len(community_avgenergy) > 0:
                    community_avgenergy = reduce(lambda x, y: x + y,  map(lambda x: x['total'], community_avgenergy)) / len(community_avgenergy)
                    community_avgenergy = community_avgenergy * 1000
                else:
                    community_avgenergy = -2  # account no data


                if community_avgenergy > 0:
                    summary = BNode()
                    statistic = BNode()

                    g.add((summary, RDF.type, EU.ElectricEnergyConsumptionSummary))
                    g.add((statistic, RDF.type, EU.ElectricEnergyStatistic))

                    g.add((node, EU.consumptionSummary, summary))
                    g.add((summary, EU.energyConsumptionStatistic, statistic))

                    g.add((summary, EU.removedObservations, Literal(0)))
                    #g.add((summary, EU.numProviders, Literal()))
                    g.add((summary, EU.numObservations, Literal(nb_obs)))

                    g.add((statistic, EU.measure, EU['day-mean']))
                    g.add((statistic, EU.energyValue, Literal(community_avgenergy)))




            else:
                g.add((node, RDF.type, EU.Topic))


            g.add((node, EU.label, Literal(concept.tag.name)))
            if concept.fullname:
                g.add((node, EU.title, Literal(concept.fullname)))

            if concept.description:
                g.add((node, EU.description, Literal(concept.description)))

            if concept.linked_concept:
                g.add((node, EU.meaning, URIRef(concept.linked_concept)))

            context['json_ld'] = g.serialize(format='json-ld', indent=4)
            #print(context['json_ld'])




        #Get info about tag subsciptions:
        context['nb_sub'] = Profile.objects.filter(tags__name=context['topic']).count()
        if self.request.user.is_authenticated():
            context['is_subscribed'] = Profile.objects.filter(user=self.request.user, tags__name=context['topic']).exists()
        else:
            context['is_subscribed'] = False

        return context



######

#FIXME directly copied and modiffed from source

######
class PostDetails(DetailView):
    """
    Shows a thread, top level post and all related content.
    """
    model = Post
    context_object_name = "post"
    template_name = "post_details.html"

    def get(self, *args, **kwargs):
        # This will scroll the page to the right anchor.
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not self.object.is_toplevel:
            return HttpResponseRedirect(self.object.get_absolute_url())

        return self.render_to_response(context)

    def get_object(self):
        user = self.request.user

        obj = super(PostDetails, self).get_object()

        # Update the post views.
        Post.update_post_views(obj, request=self.request)

        # Adds the permissions
        obj = post_permissions(request=self.request, post=obj)

        # This will be piggybacked on the main object.
        obj.sub = Subscription.get_sub(post=obj, user=user)

        # Bail out if not at top level.
        if not obj.is_toplevel:
            return obj

        # Populate the object to build a tree that contains all posts in the thread.
        # Answers sorted before comments.
        thread = [post_permissions(request=self.request, post=post) for post in Post.objects.get_thread(obj, user)]

        # Do a little preprocessing.
        answers = [p for p in thread if p.type == Post.ANSWER]

        tree = OrderedDict()
        for post in thread:

            if post.type == Post.COMMENT:
                tree.setdefault(post.parent_id, []).append(post)

        store = {Vote.UP: set(), Vote.DOWN: set(), Vote.BOOKMARK: set()}

        if user.is_authenticated():
            pids = [p.id for p in thread]
            votes = Vote.objects.filter(post_id__in=pids, author=user).values_list("post_id", "type")

            for post_id, vote_type in votes:
                store.setdefault(vote_type, set()).add(post_id)

        # Shortcuts to each storage.
        bookmarks = store[Vote.BOOKMARK]
        upvotes = store[Vote.UP]
        downvotes = store[Vote.DOWN]

        # Can the current user accept answers
        can_accept = obj.author == user

        def decorate(post):
            post.has_bookmark = post.id in bookmarks
            post.has_upvote = post.id in upvotes
            post.has_downvote = post.id in downvotes
            post.can_accept = can_accept or post.has_accepted

        # Add attributes by mutating the objects
        map(decorate, thread + [obj])

        # Additional attributes used during rendering
        obj.tree = tree
        obj.answers = answers

        # Add the more like this field
        post = super(PostDetails, self).get_object()

        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetails, self).get_context_data(**kwargs)
        context['request'] = self.request

        # Create JSON-LD
        #
        # < span
        # itemscope
        # itemtype = "http://schema.org/Question" >
        # { % post_body
        # post
        # user
        # post.tree %}
        # < / span >
        #
        # {  # Render each answer for the post #}
        #    { % for answer in post.answers %}
        # < span
        # itemscope
        # itemtype = "http://schema.org/Answer" >
        #            { % post_body
        # answer
        # user
        # post.tree %}
        # < / span >
        #     { % endfor %}
        #


        #print(context['post'])

        post = context['post']

        EU = Namespace("http://socsem.open.ac.uk/ontologies/eu#")
        SIOC = Namespace("http://rdfs.org/sioc/ns#")

        node = URIRef(self.request.build_absolute_uri())
        g = Graph()

        #Main post:
        g.add((node, RDF.type, EU.Discussion))
        g.add((node, EU.title, Literal(post.title)))
        g.add((node, EU.numBookmarks, Literal(post.book_count)))
        g.add((node, EU.numViews, Literal(post.view_count)))
        g.add((node, EU.content, Literal(post.content)))
        g.add((node, EU.created, Literal(post.creation_date)))
        g.add((node, EU.modified, Literal(post.lastedit_date)))
        g.add((node, EU.numUpvotes, Literal(post.score)))
        g.add((node, SIOC.has_author, URIRef(self.request.build_absolute_uri(reverse('user-details', args=[post.author.id]))))) #post.author

        #Add tags:
        for tag in post.parse_tags():
            g.add((node, EU.concept, URIRef(self.request.build_absolute_uri(reverse('topic-list', args=[tag])))))

        #Add answers:
        for answer in post.answers:
            node2 = URIRef(self.request.build_absolute_uri() + "#" + str(answer.id))

            # Main post:
            g.add((node2, RDF.type, EU.Reply))
            g.add((node2, SIOC.reply_of, node))
            g.add((node, SIOC.has_reply, node2))

            g.add((node2, EU.numBookmarks, Literal(answer.book_count)))
            g.add((node2, EU.content, Literal(answer.content)))
            g.add((node2, EU.created, Literal(answer.creation_date)))
            g.add((node2, EU.modified, Literal(answer.lastedit_date)))
            g.add((node2, EU.numUpvotes, Literal(answer.score)))
            g.add((node2, SIOC.has_author, URIRef(
                self.request.build_absolute_uri(reverse('user-details', args=[answer.author.id])))))  # post.author

        context['json_ld'] = g.serialize(format='json-ld', indent=4)
        #print(context['json_ld'])

        return context

def data(request, slug):
    try:

        user = User.objects.get(id=slug)

        if user.is_energynote_verified is False:
            raise Http404("User does not have any data")

    except User.DoesNotExist:
        raise Http404("User does not exist")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="consumption.csv"'

    writer = csv.writer(response)

    consumption_set = EnergyConsumption.objects.filter(email=user.energynote_email)
    writer.writerow(['t', 'concept', 'consumption'])
    for consumption in consumption_set:
        writer.writerow([consumption.timestamp, consumption.concept, consumption.consumption])

    return response


