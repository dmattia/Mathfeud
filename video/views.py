from django.shortcuts import render, render_to_response
from video.models import *
# Create your views here.

def getVideos(request):
        return render(request, 'main/videos.html', {'videos': Video.objects.order_by('grade')})

def getVideo(request, vidNumber):
        return render(request, 'main/video.html', {'video': Video.objects.get(id=vidNumber)})
