from django.db import models
from django.contrib import admin

# Create your models here.
class Video(models.Model):
        url = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
	topic = models.ForeignKey('Topic')
        def __unicode__(self):
                return self.name
	@property
	def grade(self):
		t = Topic.objects.get(name=self.topic.name)
		return t.grade
        @property
        def getEmbedUrl(self):
                return self.url.replace("watch?v=","embed/",1) + "?modestbranding=1"

class Topic(models.Model):
	name = models.CharField(max_length=255)
	grade = models.IntegerField()
	def __unicode__(self):
		return self.name

admin.site.register(Video)
admin.site.register(Topic)
