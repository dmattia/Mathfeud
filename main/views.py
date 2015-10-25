from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from main.forms import GroupProfileForm, GroupReadOnlyForm
from .models import UserProfile, GroupProfile
import json

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def profile(request):
    context_dict = {}
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict['user'] = request.user
    context_dict['group'] = user_profile.group
    return render(request, 'main/profile.html', context_dict)

def send_invite(request):
	invite_email = None
	if request.method == 'POST':
		invite_email = request.POST.get('invite_email')
		response_data = {}

		subject = "Mathfeud Invite"
		user_profile = UserProfile.objects.get(user=request.user)
		message = "Active your account for group " + user_profile.group.name + "at " + request.build_absolute_uri(reverse('member_register')) + "?group_name=" +  user_profile.group.name
		#test if the email address is valid
		try:	
			send_mail(subject, message, 'mathfeud@psychstat.org', [invite_email], fail_silently=False)
			response_data['result'] = 'Get email successfully!'
			response_data['status'] = '1'
		except:
			response_data['result'] = 'Did not sent out email!'
			response_data['status'] = '0'
		response_data['group'] = user_profile.group.name
		return HttpResponse(
			json.dumps(response_data),
			content_type = "application/json"
		)
	else:
		return HttpResponse(
			json.dumps({"nothing to see": "this isn't happening"}),
			content_type = "application/json"
		)
"""
def getVideos(request):
	return render_to_response('main/videos.html', {'videos': Video.objects.order_by('grade')})

def getVideo(request, vidNumber):
	return render_to_response('main/video.html', {'video': Video.objects.get(id=vidNumber)})
"""
