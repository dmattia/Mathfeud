from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.db import models
from PIL import Image, ImageOps
from django.core.cache import cache
from django.core.mail import send_mail

def view_page(user, pageViewed, idViewed=0):
	""" Updates that @user has visited @pageViewed
	    by creating a UserActivityLog object.
	    Sends an email to dmattia@nd.edu if this
	    is an important log piece
	Params:
	    @user: user that viewed a page
	    @pageViewed: page that @user viewed
	Returns:
	    none
	"""

	"""
	send_mail('Mathfeud Update',
		'%s viewed %s' % (user.username, pageViewed),
		'updates@mathfeud.org',
		['dmattia@nd.edu'],
		fail_silently = False)
	"""
	new_log = UserActivityLog()
	new_log.user = user
	new_log.page_viewed = pageViewed
	new_log.id_viewed = idViewed
	new_log.save()

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

class UserActivityLog(models.Model):
	LOGGED_IN = 'LOGIN'
	VIDEOS = 'VIDOS'
	VIDEO = 'VIDEO'
	BLOG_LIST = 'BLOGS'
	BLOG = 'BLOG'
	PROFILE = 'PROF'
	QUIZ = 'QUIZ'
	HOME = 'HOME'
	TOPICS = 'TOPIC'
	QA = 'QA'
	QALIST = 'QLIST'
	PAGE_VIEWED_CHOICES = (
		(LOGGED_IN, 'Logged in'),
		(VIDEOS, 'Videos'),
		(VIDEO, 'Video'),
		(BLOG_LIST, 'Blogs'),
		(BLOG, 'Blog'),
		(PROFILE, 'Profile'),
		(QUIZ, 'Quiz'),
		(HOME, 'Home'),
		(TOPICS, 'Topics'),
		(QA, 'Question Answer'),
		(QALIST, 'Question Answer List'),
	)
	user = models.ForeignKey(User)
	page_viewed = models.CharField(max_length=5, choices=PAGE_VIEWED_CHOICES, default=LOGGED_IN)
	time = models.DateTimeField(auto_now=True)
	id_viewed = models.IntegerField()

	def __unicode__(self):
		return "%s viewed %s" % (self.user, self.page_viewed)

class UserActivityLogAdmin(admin.ModelAdmin):
	readonly_fields = ('time',)

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	group = models.ForeignKey(GroupProfile)
	picture = models.ImageField(upload_to='/mathfeud/mathfeud/images/profile_photos/', null=True)
	score = models.IntegerField(default=0)
	def __unicode__(self):
		return self.user.username
	def picture_path(self):
		if self.picture:
			return self.picture.url.replace('/mathfeud/mathfeud','',1)
		else:
			return False
	def last_seen(self):
		return cache.get('seen_%s' % self.user.username)
	def online(self):
		if self.last_seen():
			now = datetime.datetime.now()
			if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
				return False
			else:
				return True
		else:
			return False

	'''
	def save(self):
		if not self.picture:
			return

		super(UserProfile, self).save()

	        image = Image.open(self.picture)
	        (width, height) = image.size
	
	        "Max width and height 512"        
	        if (512 / width < 512 / height):
	            factor = 512 / height
	        else:
	            factor = 512 / width
	
	        size = ( width / factor, height / factor)
	        image = image.resize(size, Image.ANTIALIAS)
	        image.save(self.photo.path)
	'''

class PendingInvite(models.Model):
	group = models.ForeignKey(GroupProfile)
	email = models.CharField(max_length=50)
	activation_key = models.CharField(max_length=40)
	def __unicode__(self):
		return "Pending invite for %s" % self.email

admin.site.register(GroupProfile)
admin.site.register(UserProfile)
admin.site.register(UserActivityLog, UserActivityLogAdmin)
admin.site.register(PendingInvite)
