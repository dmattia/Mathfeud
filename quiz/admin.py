from django.contrib import admin
from .models import QuestionResponse

# Register your models here.
class QuestionResponseAdmin(admin.ModelAdmin):
	"""Allows the time field for a question to be
	displayed on the admin site
	"""
	readonly_fields = ('time',)

admin.site.register(QuestionResponse, QuestionResponseAdmin)
