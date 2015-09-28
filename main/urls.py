from django.conf.urls import patterns, url
from main import views

urlpatterns = [ url(r'^$', views.index, name='index'),
	url(r'userProfile', views.profile, name='user_profile')
]

