from django.db import models
from main.models import GroupProfile, UserProfile
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib import admin

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=60)
    body = RichTextField()
    poster = models.ForeignKey(UserProfile, null=True)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title

class Answer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(UserProfile, null=True)
    body = RichTextField()
    question = models.ForeignKey(Question)
    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))

admin.site.register(Question)
admin.site.register(Answer)
