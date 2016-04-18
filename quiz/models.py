from django.db import models
from django import forms
from django.contrib import admin
from video.models import Video, Topic
from main.models import UserProfile
import random

class AutoQuestion(models.Model):
	""" An auto generated question based on an equation
		and a number of variables in that equation
	"""
	equation = models.CharField(max_length=255)
	varCount = models.IntegerField()
	topic = models.ForeignKey(Topic)
	
	def getExpression(self):
		expression = self.equation.rpartition('=')[0]
		return expression.strip()

	def generate(self):
		newExpr = self.getExpression()
		for i in xrange(self.varCount-1):
			newExpr = newExpr.replace("{" + str(i+1) + "}", str(random.randint(0,100)))
		return newExpr

	def solveExpr(self):
		expression = self.generate()
		solution = eval(expression)
		return solution

	def __init__(self, equation, varCount):
		self.equation = equation
		self.varCount = varCount

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

class QuestionResponse(models.Model):
	"""A response to a quiz question.
	
	@user: The user who answered the question
	@question: The question that was answered
	@correct: True if the user answered the question correctly
	@time: The time of this submission
	"""
	user = models.ForeignKey('main.UserProfile')
	question = models.ForeignKey('Question')
	correct = models.BooleanField()
	time = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return unicode("%s response to: \"%s\"" % (self.user, self.question))

admin.site.register(AutoQuestion)
admin.site.register(Question)
admin.site.register(Answer)
