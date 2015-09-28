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

admin.site.register(GroupProfile)
admin.site.register(UserProfile)
