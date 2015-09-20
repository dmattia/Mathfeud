from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
	url(r'^$', views.main, name='blogList'),
	url(r'^(\d+)/$', views.post, name='post'),
	url(r'^add_comment/(\d+)/$', views.add_comment, name='add_comment'),
	)
