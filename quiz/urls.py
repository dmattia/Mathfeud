from django.conf.urls import patterns, url
from quiz import views

urlpatterns = patterns('',
        url(r'^$', views.all_questions, name='questionList'),
	)
