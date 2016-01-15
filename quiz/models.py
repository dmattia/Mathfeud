from django.db import models
from django.contrib import admin
from video.models import Video
from django import forms

class Question(models.Model):
	"""A Question to be asked along with a particular video

	@question_text is the text to be displayed for this question
	@video is the video that this question belongs to
	"""
	question_text = models.CharField(max_length=255)
	video_ref = models.ForeignKey('video.Video')

	def __unicode__(self):
		return unicode("%s" % (self.question_text))

	def answer_set(self):
		return Answer.objects.filter(question_ref=self)

class Answer(models.Model):
	"""A possible answer to a Question

	@question_ref is a pointer to a Question
	@answer_text is the text to be displayed for this Answer
	@correct is a boolean for if this answer is a correct answer or not
	"""
	question_ref = models.ForeignKey('Question')
	answer_text = models.CharField(max_length=255)
	correct = models.BooleanField()

	def __unicode__(self):
		if self.correct:
			correct_str = "Correct"	
		else:
			correct_str = "Incorrect"	
		return unicode("%s answer to question: %s" % (correct_str, self.question_ref.question_text))

admin.site.register(Question)
admin.site.register(Answer)
