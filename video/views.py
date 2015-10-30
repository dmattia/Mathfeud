from django.shortcuts import render, render_to_response
from video.models import *
# Create your views here.

def topicList(request):
	return render(request, 'main/topics.html', {'topics': Topic.objects.all().order_by('grade')})

def getVideos(request, topicName):
        return render(request, 'main/videos.html', {'videos': Video.objects.filter(topic=Topic.objects.get(name=topicName))})

def getVideo(request, vidNumber):
        return render(request, 'main/video.html', {'video': Video.objects.get(id=vidNumber)})
