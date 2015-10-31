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
	picture = models.ImageField(upload_to='/mathfeud/mathfeud/images/profile_photos/', null=True)
	def __unicode__(self):
		return self.user.username
	def picture_path(self):
		return self.picture.url.replace('/mathfeud/mathfeud','',1)

class PendingInvite(models.Model):
	group = models.ForeignKey(GroupProfile)
	email = models.CharField(max_length=50)
	activation_key = models.CharField(max_length=40)
	def __unicode__(self):
		return "Pending invite for %s" % self.email

admin.site.register(GroupProfile)
admin.site.register(UserProfile)
admin.site.register(PendingInvite)
