from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Video(models.Model):
        url = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
	topic = models.ForeignKey('Topic')
	description = models.CharField(max_length=2000)
	add_time = models.DateTimeField(auto_now=True, blank=True)
        def __unicode__(self):
                return self.name
	@property
	def grade(self):
		t = Topic.objects.get(name=self.topic.name)
		return t.grade
        @property
        def getEmbedUrl(self):
                return self.url.replace("watch?v=","embed/",1) + "?modestbranding=1"
	@property
	def videoID(self):
		return self.url.replace("https://www.youtube.com/watch?v=","",1)

class Topic(models.Model):
	name = models.CharField(max_length=255)
	grade = models.IntegerField()
	order_value = models.IntegerField() #To create an order of the topics. Smaller will appear first
	def __unicode__(self):
		return self.name

class VideoComment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	poster = models.ForeignKey(User)
	body = RichTextField()
	post = models.ForeignKey(Video)

	def __unicode(self):
		return unicode("%s: %s" % (self.post, self.body[:60]))

admin.site.register(Video)
admin.site.register(Topic)
admin.site.register(VideoComment)
