from django.conf.urls import patterns, url
from video import views

urlpatterns = [ 
	url(r'^$', views.topicList, name='topics'),
        url(r'^([^/]+)/$', views.getVideos, name='videos'),
        url(r'^.+/(\d+)/$', views.getVideo, name='video'),
        url(r'^.+/(\d+)/quiz/$', views.getVideoQuiz, name='quiz'),
	url(r'^returnToPrevPage/$', views.returnToPrevPage, name='returnToPrevPage'),
]
