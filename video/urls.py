from django.conf.urls import patterns, url
from video import views

urlpatterns = [ 
        url(r'^$', views.getVideos, name='videos'),
        url(r'^(\d+)/$', views.getVideo, name='video'),
]
