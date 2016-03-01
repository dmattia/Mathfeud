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
    solved = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title

class Answer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(UserProfile, null=True)
    body = RichTextField()
    score = models.IntegerField(default=0)
    isBestAnswer = models.BooleanField(default=False)
    question = models.ForeignKey(Question)
    def __unicode__(self):
        return unicode("%s: %s" % (self.question.title, self.body[:60]))

class Votes(models.Model):
    """
    @voter: user who voted
    @answer: the specific answer being voted
    @up: true if upvote, false if downvote
    """
    voter = models.ForeignKey(UserProfile, null=True)
    answer = models.ForeignKey(Answer)
    up = models.BooleanField()
    def __unicode__(self):
	return unicode("%s vote on %s" % (self.voter.user.username, self.answer.body[:60]))

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Votes)
