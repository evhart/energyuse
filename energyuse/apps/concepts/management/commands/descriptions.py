from django.core.management.base import BaseCommand, CommandError
import json
import os
import re
import tempfile
import urllib
from urlparse import urlparse
from biostar.apps.posts.models import Vote, Post, Tag
from energyuse.apps.concepts.models import Concept
from energyuse.apps.eusers.models import User
import requests
from filer.models import Image
from django.core.files import File


class Command(BaseCommand):
    help = 'Generate tag descriptions using DBPedia Spotlight and DBPedia Abstracts'

    proxies = { "http": "http://wwwcache.open.ac.uk:80",
                "https": "http://wwwcache.open.ac.uk:80"}

    #proxies = {}

    def annotate(self, entity, appliance, concept):
        #Get the DBPedia info:
        #proxies={}



        #print(dbpedia_info[entity])
        try:

            dbpedia_info = json.loads(
                requests.get(entity.replace("/resource/", "/data/") + ".json", proxies=self.proxies).text)


            name = [name['value'] for name in dbpedia_info[entity]["http://www.w3.org/2000/01/rdf-schema#label"] if name['lang'] == 'en'][0]

            abstract = [abstract['value'] for abstract in dbpedia_info[entity]["http://dbpedia.org/ontology/abstract"] if abstract['lang'] == 'en'][0]
            if dbpedia_info[entity]["http://www.w3.org/2000/01/rdf-schema#comment"]:
                abstract = [abstract['value'] for abstract in dbpedia_info[entity]["http://www.w3.org/2000/01/rdf-schema#comment"] if abstract['lang'] == 'en'][0]

            thumbnail = None
            image_tmp = tempfile.NamedTemporaryFile(delete=False)
            try:
                thumbnail = [thumbnail['value'] for thumbnail in dbpedia_info[entity]["http://dbpedia.org/ontology/thumbnail"]][0]
                thumbnail = thumbnail[:thumbnail.rfind('?')]
                thumbnail = thumbnail.replace("/thumb/", "")
                image_tmp.write(requests.get(thumbnail, proxies=self.proxies).content)

                image_tmp.close()
            except:
                 pass

            print(name)
            print(abstract)
            print(thumbnail)

            #if 0 == 0:
            if concept.description == "" or concept.description is None:
                concept.description = "<p>" + abstract + \
                                        "</p><p>Description automatically generated from <a href=\"" + \
                                              entity + "\">DBPedia</a>.</p>"

                if thumbnail:
                    with open(image_tmp.name, 'r') as f:
                        image_name = urlparse(thumbnail).path.split('/')[-1]
                        image_file = File(f)
                        image = Image.objects.create(name=image_name,file=image_file)
                        concept.image = image

                concept.fullname = name
                concept.generated = True
                concept.linked_concept = entity
                concept.appliance = appliance
                concept.save()

            os.remove(image_tmp.name)
        except:
            pass


    def is_appliance(self, entity):
        if entity == "":
            return 0

        url = 'http://dbpedia.org/sparql'
        query = "ASK { <" + entity + "> _:_ <http://dbpedia.org/resource/Category:Home_appliances> }"
        params = {"default-graph-uri": "http://dbpedia.org",
                  "format": "application/sparql-results+json",
                  "query": query}

        response = requests.get(url, params=params, proxies=self.proxies)
        # print(response.text)
        j = json.loads(response.text)

        # return j['boolean']
        if j['boolean']:
            return 1
        return 0

    def wiki(self, label):
        linked_entity = ""

        url = 'https://en.wikipedia.org/w/api.php'
        params = {"action": "opensearch", "search": label.replace("-", "+"), "limit": "1", "format": "json"}
        headers = {'Accept': 'application/json'}
        response = requests.get(url, params=params, headers=headers, proxies=self.proxies)
        j = json.loads(response.text)

        if (j[3]):
            linked_entity = j[3][0].replace("https://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")

            # Lookup redirect:
            url = 'http://dbpedia.org/sparql'
            query = "SELECT ?preferred_uri WHERE { <" + linked_entity + "> <http://dbpedia.org/ontology/wikiPageRedirects> ?preferred_uri . }"
            params = {"default-graph-uri": "http://dbpedia.org",
                      "format": "application/sparql-results+json",
                      "query": query}

            response = requests.get(url, params=params, proxies=self.proxies)
            j = json.loads(response.text)

            if j['results']['bindings']:
                linked_entity = j['results']['bindings'][0]['preferred_uri']['value']

        print label + " -> " + linked_entity
        return {'label': label, 'entity': linked_entity, 'app': self.is_appliance(linked_entity)}

    def handle(self, *args, **options):

        annotations = []
        for concept in Concept.objects.all():
            label = concept.tag.name

            posts = Post.objects.filter(tag_val__contains=label, type=0)
            print(posts)

            # posts = Post.objects.filter(tag_val__contains=concept.tag.name, type=0)
            if posts:
                # txt = reduce(lambda x, y: x.title.encode('utf8') + " " + x.content.encode('utf8') + " " + y.title.encode('utf8')+ " " + y.content.encode('utf8'), posts)
                # txt = reduce(lambda x, y: str(x.title) + " " + str(x.content.encode('utf8')) + " " + str(y.title) + " " + str(y.content.encode('utf8')),posts)
                # txt = reduce(lambda x, y: x.content.encode('ascii', 'ignore') + y.content.encode('ascii', 'ignore'),posts)

                txt = label + " "
                for post in posts:
                    txt += post.title + " " + post.content + " "

                # Get the entity associated with the label:
                url = 'http://socsem.open.ac.uk/spotlight/rest/annotate'
                #url = 'http://spotlight.sztaki.hu:2222/rest/annotate'
                params = {"text": txt, "confidence": 0.4, "support": 20}
                headers = {'Accept': 'application/json'}
                response = requests.get(url, params=params, headers=headers, proxies=self.proxies)
                j = json.loads(response.text)

                # Get resource
                # print j
                linked_entity = ""
                if j and j.has_key('Resources') and j['Resources'][0]['@offset'] == "0":
                    linked_entity = j['Resources'][0]["@URI"]
                    annotations.append(
                        {'label': label, 'entity': linked_entity, 'app': self.is_appliance(linked_entity)})


                # Do a Wikipedia search:
                else:
                    result = self.wiki(label)
                    annotations.append(result)

            else:
                print("No posts found for '" + label + "' (Using OpenSearch).")
                result = self.wiki(label)
                annotations.append(result)

            self.annotate(result['entity'], result['app'], concept)