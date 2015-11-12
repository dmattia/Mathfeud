from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from video.models import VideoComment

class VideoCommentForm(forms.ModelForm):
	class Meta:
		model = VideoComment
		fields = ['body']
