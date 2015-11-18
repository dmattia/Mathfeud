from django.db import models
from django.contrib import admin

# Create your models here.
class MultipleChoiceQuestion(models.Model):
	# Will eventually need to create a model for a question with auto-generated variables
	question = models.CharField(max_length=255)
	option1 = models.CharField(max_length=255)
	option2 = models.CharField(max_length=255)
	option3 = models.CharField(max_length=255)
	option4 = models.CharField(max_length=255)
	answer = models.IntegerField()

	def __unicode__(self):
		return unicode("%s" % (self.question))

admin.site.register(MultipleChoiceQuestion)
