from django.conf.urls import patterns, url
from qa import views

urlpatterns = patterns('',
        url(r'^$', views.main, name='qaList'),
	url(r'^newQuestion/$', views.NewQuestion, name='newQuestion'),
	url(r'^add_question/$', views.add_question, name='add_question'),
	url(r'^(\d+)/$', views.question, name='question'),
	url(r'add_answer/(\d+)/$', views.add_answer, name='add_answer'),
	)
