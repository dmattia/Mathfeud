from django.shortcuts import render, render_to_response
from video.models import *
from video.forms import VideoCommentForm
from main.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def topicList(request):
	allTopics = Topic.objects.all().order_by('grade').order_by('order_value')
	topicsWithVideos = []
	for topic in allTopics:
		if len(Video.objects.filter(topic=topic)) > 0:
			topicsWithVideos.append(topic)
	return render(request, 'main/topics.html', {'topics': topicsWithVideos})

@login_required
def getVideos(request, topicName):
	params = {
		'videos': Video.objects.filter(topic=Topic.objects.get(name=topicName)),
		'topic': topicName,
	}
        return render(request, 'main/videos.html', params)

@login_required
def getVideo(request, vidNumber):
	video = Video.objects.get(id=vidNumber)

	if request.method == 'POST':
		form = VideoCommentForm(request.POST)
		if form.is_valid():
			newComment = VideoComment()
			newComment.poster = request.user
			newComment.post = video
			newComment.body = form.cleaned_data['body']
			newComment.save()
		form = VideoCommentForm()
	else:
		form = VideoCommentForm()
		
	args = {
		'video': video,
		'comments': VideoComment.objects.filter(post=video),
		'myform': form,
	}
        return render(request, 'main/video.html', args)
