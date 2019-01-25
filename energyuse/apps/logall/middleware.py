import time
import simplejson as json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from types import NoneType
from energyuse.apps.logall.models import Record


class LogAllMiddleware(object):

    def process_request(self,request):
        # Only log requests of authinticate users
        # try:
        #     if not request.user.is_authenticated():
        #         return None
        # except AttributeError:
        #     return None


        user = None
        try:
             if request.user.is_authenticated():
                 user = request.user
        except AttributeError:
             user = None



        # Skip favicon requests cause I do not care about them
        if request.path =="/favicon.ico":
            return None

        newRecord = Record(
            created_at = str(time.time()),
            sessionId = request.session.session_key,

            requestUser = user,
            requestPath  = request.path,
            requestQueryString = request.META["QUERY_STRING"],
            requestVars = json.dumps(request.REQUEST.__dict__),
            requestMethod = request.method,
            requestSecure = request.is_secure(),
            requestAjax = request.is_ajax(),
            #requestMETA = request.META.__str__(),
            requestAddress = request.META["REMOTE_ADDR"],
            )

        if(request.session.session_key is not None):
            newRecord.save()

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        # try:
        #     if not request.user.is_authenticated():
        #         return None
        # except AttributeError:
        #     return None
        user = None
        try:
             if request.user.is_authenticated():
                 user = request.user
        except AttributeError:
             user = None

        # Fix the issue with the authrization request
        try:
            theRecord  = Record.objects.filter(
                sessionId = request.session.session_key,
                requestUser = user,
                requestPath  = request.path,
                requestMethod = request.method,
                requestSecure = request.is_secure(),
                requestAjax = request.is_ajax()#,
                #requestMETA = request.META.__str__()
                ).last()

            #if(view_func is not None or view_func is not NoneType):
            #    if hasattr(view_func, 'func_name'):
                    #theRecord.viewFunction = view_func.func_name
                    #theRecord.viewDocString = view_func.func_doc
                    #theRecord.viewArgs = json.dumps(view_kwargs)

            #theRecord.save()

        except ObjectDoesNotExist or MultipleObjectsReturned or AttributeError:
            pass

        return None


    def process_response(self, request, response):

        # Only log autherized requests
        # try:
        #     if not request.user.is_authenticated():
        #         return response
        # except AttributeError:
        #     return response
        user = None
        try:
             if request.user.is_authenticated():
                 user = request.user
        except AttributeError:
             user = None

        # Skip favicon requests cause I do not care about them
        if request.path =="/favicon.ico":
            return response



        if not hasattr(request, 'user'):
            return response

        # Fix the issue with the authorization request
        try:
            theRecord  = Record.objects.filter(
                sessionId = request.session.session_key,
                requestUser = user,
                requestPath  = request.path,
                requestMethod = request.method,
                requestSecure = request.is_secure(),
                requestAjax = request.is_ajax()#,
                #requestMETA = request.META.__str__()
                ).last()

            if(theRecord is not None):
                theRecord.responseCode = response.status_code
                theRecord.save()

        except  ObjectDoesNotExist or MultipleObjectsReturned:
            pass

        return response