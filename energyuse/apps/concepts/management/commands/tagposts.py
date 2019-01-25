from django.core.management.base import BaseCommand, CommandError
import json
import re
import urllib
from biostar.apps.posts.models import Vote, Post, Tag
from energyuse.apps.concepts.models import Concept
from energyuse.apps.eusers.models import User
import requests

class Command(BaseCommand):
    help = 'Generate new tags using the http://services.gate.ac.uk/decarbonet/term-recognition/'

    def levenshtein(self, s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t:
            return 0
        elif len(s) == 0:
            return len(t)
        elif len(t) == 0:
            return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(t)]

    def handle(self, *args, **options):

        # Get all the question posts
        for post in Post.objects.filter(type__in=Post.TOP_LEVEL):
            try:
                # post.author.score = post.author.score + post.score
                # post.author.save()
                # print(post.title + re.sub('<[^<]+?>', '', post.content))

                # Get all the annotation terms:
                content = post.title + re.sub('<[^<]+?>', '', post.content)
                params = urllib.urlencode({'text': content})
                f = urllib.urlopen("http://services.gate.ac.uk/decarbonet/term-recognition/service", params)
                j = json.loads(f.read())
                # print(j['entities']['Term'])

                # Get the current tags associated with the post:
                current_tags = post.parse_tags()

                # Add tags:
                for term in j['entities']['Term']:
                    # print term
                    # print content[term['indices'][0]:term['indices'][1]]

                    # Convert the term URI to the correct GEMMET description:
                    # http://www.eionet.europa.eu/gemet/getConcept?concept_uri=http://www.eionet.europa.eu/gemet/concept/95&language=en
                    if term['rule'] == 'Gemet':
                        params2 = urllib.urlencode({'concept_uri': term['Instance'], 'lang': 'en'})
                        f2 = urllib.urlopen("http://www.eionet.europa.eu/gemet/getConcept", params2)
                        j2 = json.loads(f2.read())

                        label = j2['preferredLabel']['string'].replace(" ", "-").lower()
                        title = j2['preferredLabel']['string']
                        definition = j2['definition']['string']
                        # print(label)
                        # print(definition)

                        #if 0 == 0:
                        if not (label in current_tags):
                            print label

                            # Add tag:
                            exists = False
                            for tag in current_tags:
                                if self.levenshtein(tag, label) < 3:
                                    exists = True

                            if not exists:
                                print("Adding (Gemet)..." + label)
                                current_tags.extend([label])

                                post.add_tags(",".join(current_tags))
                                post.tag_val = ",".join(current_tags)
                                post.save()

                                # Check if tag already in the database, if not create tag:
                                # concept = Concept.objects.get(tag__name=label)
                                # if concept.description == "" or concept.description is None:
                                #     concept.description = "<p>" + definition + \
                                #                           "</p><p>Description automatically generated from the <a href=\"" + \
                                #                           term['Instance'] + "\">GEMET Thesaurus</a>.</p>"
                                #     concept.fullname = title.title()
                                #     concept.generated = True
                                #     concept.linked_concept = term['Instance']
                                #     concept.save()
                                #     print(concept)

                    #Appliance Annotation
                    txt = content
                    # print txt

                    url = 'http://socsem.open.ac.uk/spotlight/rest/annotate'
                    sparql = "SELECT DISTINCT ?appliance WHERE { ?appliance ?related <http://dbpedia.org/resource/Category:Home_appliances> }"
                    params = {"text": txt, "confidence": 0.4, "support": 20, "sparql": sparql}
                    headers = {'Accept': 'application/json'}
                    response = requests.get(url, params=params, headers=headers)
                    j = json.loads(response.text)

                    label = None
                    exists = False
                    if j and j.has_key('Resources') and j['Resources'][0]:
                        linked_entity = j['Resources'][0]["@URI"]
                        label = j['Resources'][0]["@surfaceForm"].replace(" ", "-").lower()

                        # Check if a similar label is not already present:
                        tags = post.parse_tags()
                        for tag in current_tags:
                            if self.levenshtein(tag, label) < 3:
                                exists = True
                    # if label:
                    #    print label
                    if not exists and label:
                        print("Adding (Spotlight)..."+label)
                        current_tags.extend([label])

                        post.add_tags(",".join(current_tags))
                        post.tag_val = ",".join(current_tags)
                        post.save()

                        # #####

            except:
                pass

        self.stdout.write('Done...')
