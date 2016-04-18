from django.conf.urls import patterns, url
from main import views
from video import views as video_views
#from qa import views as qa_views

urlpatterns = [ 
	url(r'^$', video_views.home, name='index'),
	url(r'userProfile', views.profile, name='user_profile'),
	url(r'^send_invite/$', views.send_invite, name='send_invte'),
	#url(r'qa', qa_views.main , name='qa'),
	url(r'^json', views.jsonView),
]

