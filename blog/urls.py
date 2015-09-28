from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
	url(r'^$', views.main, name='blogList'),
	url(r'^(\d+)/$', views.post, name='post'),
	url(r'^add_comment/(\d+)/$', views.add_comment, name='add_comment'),
	url(r'^newPost/$', views.NewPost, name='newPost'),
	url(r'add_post/$', views.add_post, name='add_post'),
	url(r'^date/$', views.get_date, name='date page')
	)
