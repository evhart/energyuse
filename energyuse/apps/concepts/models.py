from biostar.apps.posts.models import Tag
from django.contrib import admin
from django.db import models
from filer.fields.image import FilerImageField

# Create concepts when tag is created OR when page is accessed ?
# User tags are managed outside post tags.....
class Concept(models.Model):
    icon = FilerImageField(null=True, blank=True, related_name="concept_icon")
    image = FilerImageField(null=True, blank=True, related_name="concept_image")
    fullname = models.CharField(null=True, max_length=50, blank=True)
    description = models.TextField(null=True, blank=True)
    appliance = models.BooleanField(default=False)
    image_source = models.CharField(max_length=50, null=True, blank=True)
    image_author = models.CharField(max_length=50, null=True, blank=True)
    tag = models.OneToOneField(Tag, null=True, blank=True)
    generated = models.BooleanField(default=False)
    linked_concept = models.URLField(null=True, blank=True)

    @staticmethod
    def auto_create(sender, instance, created, *args, **kwargs):
        "Should run on every tag creation."
        if created:
            c = Concept(tag=instance)
            c.save()

    def __str__(self):
        if self.fullname:
            return str(self.fullname).title()
        else:
            return str(self.tag.name).title()


from django.db.models.signals import post_save
post_save.connect(Concept.auto_create, sender=Tag)

class ConceptAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'description')
    search_fields = ['fullname']


admin.site.register(Concept, ConceptAdmin)