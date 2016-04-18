from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from main.forms import GroupProfileForm, GroupReadOnlyForm, UpdateProfilePictureForm
from .models import UserProfile, GroupProfile, PendingInvite, UserActivityLog, view_page

import json
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from qa import models as qa_models
from blog import models as blog_models
from video import models as video_models

import hashlib
import random
import re

# Create your views here.
def index(request):
    view_page(request.user, UserActivityLog.HOME)
    params = {
        'videos': Videos.objects.all(),
    }
    return render(request, 'main/home.html', {})

def profile(request):
    view_page(request.user, UserActivityLog.PROFILE)

    user_profile = UserProfile.objects.get(user=request.user)

    #send_mail("try", "message", 'mathfeud@psychstat.org', ['xwang29@nd.edu'], fail_silently=False)
    if request.method == 'POST':
        p = request.POST
        form = UpdateProfilePictureForm(p, request.FILES)
        if form.is_valid():
            newPic = form.cleaned_data['newPic']
            user_profile.picture = newPic            
            user_profile.save()
    else:
        form = UpdateProfilePictureForm()

    context_dict = {}
    context_dict['user'] = request.user
    context_dict['user_profile'] = user_profile
    context_dict['group'] = user_profile.group
    context_dict['form'] = form
    context_dict['is_admin'] = request.user.groups.filter(name='groupAdmin').exists()
    context_dict['group_members'] = UserProfile.objects.filter(group=user_profile.group)

    getScore(user_profile)
    context_dict['recent_videos'], context_dict['recent_questions'], context_dict['recent_blogs'] = getActivity(user_profile)

    context_dict['new_videos'] = getUpdate()
    context_dict['user_questions'] = qa_models.Question.objects.filter(poster=user_profile)
    context_dict['user_blogs'] = blog_models.Post.objects.filter(poster=request.user)
    if (context_dict['is_admin']):
        context_dict['pending_invite'] = PendingInvite.objects.filter(group=user_profile.group)
    return render(request, 'main/profile.html', context_dict)

def getUpdate():
    """
    get recent site updates
    """
    videos = video_models.Video.objects.order_by('-add_time')[:3]
    return videos

def getActivity(user_profile):
    """
    get recent viewed videos 
    """
    video_log = UserActivityLog.objects.filter(user=user_profile.user).filter(page_viewed=UserActivityLog.VIDEO).order_by('-time').values_list('id_viewed', flat=True).distinct()
    question_log = UserActivityLog.objects.filter(user=user_profile.user).filter(page_viewed=UserActivityLog.QA).order_by('-time').values_list('id_viewed', flat=True).distinct()
    blog_log = UserActivityLog.objects.filter(user=user_profile.user).filter(page_viewed=UserActivityLog.BLOG).order_by('-time')[:3]
    if len(video_log) > 3:
        video_log = video_log[:3]
    if len(question_log) > 3:
        question_log = question_log[:3]
    videos = []
    questions = []
    blogs = []
    for v in video_log:
	try:
            videos.append(video_models.Video.objects.get(pk=v))
        except:
            None
    for q in question_log:
        try:
            questions.append(qa_models.Question.objects.get(pk=q))
        except:
           None

    return videos, questions, blogs

def getScore(user_profile):
    """
    calculate current user score, store it in database and return the score
    """
    num_questions = qa_models.Question.objects.filter(poster=user_profile).count()
    num_videos_viewed = UserActivityLog.objects.filter(user=user_profile.user).filter(page_viewed=UserActivityLog.VIDEO).count()
	
    score = 2*num_questions + num_videos_viewed
    user_profile.score = score
    user_profile.save()	

def create_activation_key():
    #salt = hashlib.sha1(six.text_type(random.random()).encode('ascii')).hexdigest()[:5]
    #salt = salt.encode('ascii')
    #activation_key = hashlib.sha1(salt).hexdigest()
    return get_random_string(length=12, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def is_valid_email(invite_email):
	pending_invites = PendingInvite.objects.filter(email = invite_email)
	registered_users = User.objects.filter(email = invite_email)
	if (pending_invites.exists()):
		return False, "Invitation already sent!"
	if (registered_users.exists()):
		return False, "Email already registered!"

def send_invite(request):
	invite_email = None
	if request.method == 'POST':
		invite_email = request.POST.get('invite_email')
		response_data = {}

		subject = "Mathfeud Invite"
		user_profile = UserProfile.objects.get(user=request.user)
		activation_key = create_activation_key()
		#activation_key = "1"
		message = "Active your account for group " + user_profile.group.name + "at " + request.build_absolute_uri(reverse('member_register')) + "?group_name=" +  activation_key
		#test if the email address is valid
		is_valid, email_error_message = is_valid_email(invite_email)
		if (not is_valid):
			response_data['result'] = email_error_message
			response_data['status'] = '0'
			return HttpResponse(
				json.dumps(response_data),
				content_type = "application/json"
			)
		try:	
			send_mail(subject, message, 'mathfeud@psychstat.org', [invite_email], fail_silently=False)
			response_data['result'] = 'Get email successfully!'
			response_data['status'] = '1'
			pending_invite = PendingInvite.objects.create(group=user_profile.group, email=invite_email, activation_key=activation_key)
			pending_invite.save()
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

def jsonView(request):
	response_data = {
    "activities-heart": [
        {
            "dateTime": "2015-08-04",
            "value": {
                "customHeartRateZones": [],
                "heartRateZones": [
                    {
                        "caloriesOut": 740.15264,
                        "max": 94,
                        "min": 30,
                        "minutes": 593,
                        "name": "Out of Range"
                    },
                    {
                        "caloriesOut": 249.66204,
                        "max": 132,
                        "min": 94,
                        "minutes": 46,
                        "name": "Fat Burn"
                    },
                    {
                        "caloriesOut": 260,
                        "max": 160,
                        "min": 132,
                        "minutes": 20,
                        "name": "Cardio"
                    },
                    {
                        "caloriesOut": 135,
                        "max": 220,
                        "min": 160,
                        "minutes": 5,
                        "name": "Peak"
                    }
                ],
                "restingHeartRate": 68
            }
        }
    ]
}
 
	return HttpResponse(json.dumps(response_data), content_type="application/json")
