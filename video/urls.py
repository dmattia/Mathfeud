from django.conf.urls import patterns, url
from video import views

urlpatterns = [ 
	url(r'topics/$', views.topicList, name='topics'),
        url(r'topics/(.+)/$', views.getVideos, name='videos'),
        url(r'(\d+)/$', views.getVideo, name='video'),
]
