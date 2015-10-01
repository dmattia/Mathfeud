from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group

# Create your models here.
class GroupProfile(models.Model):
	school = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name
	@classmethod
	def create(self, name, school):
		obj = GroupProfile.objects.create(name=name, school=school)
		obj.save()
		return obj

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	group = models.ForeignKey(GroupProfile)
	def __unicode__(self):
		return self.user.username

class Video(models.Model):
	url = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	grade = models.IntegerField()
	def __unicode__(self):
		return self.name
	@property
	def getEmbedUrl(self):
		return self.url.replace("watch?v=","embed/",1) + "?modestbranding=1"

admin.site.register(GroupProfile)
admin.site.register(UserProfile)
admin.site.register(Video)
