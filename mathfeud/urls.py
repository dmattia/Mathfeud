"""mathfeud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main import regbackend
from material.frontend import urls as frontend_urls
from mathfeud import settings
#from qa import views as qa_views

urlpatterns = [
    url(r'^$', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/register/$', regbackend.MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/register/group/', regbackend.GroupMemberRegView.as_view(), name='member_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/', include('main.urls')),
    url(r'^blog/', include('blog.urls')),
    #url(r'^qa/$', qa_views.main, name='qaList'),
    url(r'^qa/', include('qa.urls')),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^videos/', include('video.urls')),
    url(r'', include(frontend_urls)),
    url(r'^images/(.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
]
