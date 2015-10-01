from django.conf.urls import patterns, url
from main import views

urlpatterns = [ url(r'^$', views.index, name='index'),
	url(r'userProfile', views.profile, name='user_profile'),
	url(r'^videos/$', views.getVideos, name='videos'),
	url(r'^videos/(\d+)/$', views.getVideo, name='video'),
]

