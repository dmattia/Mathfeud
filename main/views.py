from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from main.forms import GroupProfileForm, GroupReadOnlyForm
from .models import UserProfile, GroupProfile, PendingInvite
import json
from django.utils.crypto import get_random_string

import hashlib
import random
import re

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def profile(request):
    context_dict = {}
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict['user'] = request.user
    context_dict['user_profile'] = user_profile
    context_dict['group'] = user_profile.group
    context_dict['is_admin'] = request.user.groups.filter(name='groupAdmin').exists()
    if (context_dict['is_admin']):
        context_dict['group_members'] = UserProfile.objects.filter(group=user_profile.group)
        context_dict['pending_invite'] = PendingInvite.objects.filter(group=user_profile.group)
    return render(request, 'main/profile.html', context_dict)

def create_activation_key():
    #salt = hashlib.sha1(six.text_type(random.random()).encode('ascii')).hexdigest()[:5]
    #salt = salt.encode('ascii')
    #activation_key = hashlib.sha1(salt).hexdigest()
    return get_random_string(length=12, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

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
