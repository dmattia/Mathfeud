from django.conf.urls import patterns, url
from quiz import views

urlpatterns = patterns('',
        #url(r'(.*)/$', views.view_question, name='questionView'),
        url(r'checkSubmission/$', views.checkQuestionSubmission, name='checkSubmission'),
)
