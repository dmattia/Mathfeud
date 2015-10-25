from django.db import models
from django.contrib import admin

# Create your models here.
class Video(models.Model):
        url = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
        grade = models.IntegerField()
        def __unicode__(self):
                return self.name
        @property
        def getEmbedUrl(self):
                return self.url.replace("watch?v=","embed/",1) + "?modestbranding=1"

admin.site.register(Video)
