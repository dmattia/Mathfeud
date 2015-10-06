from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from main.forms import InviteForm
from .models import Video, UserProfile

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def profile(request):
    if request.method == 'POST':
         form = InviteForm(request.POST)
         if form.is_valid():
              invite_email = [form.cleaned_data['invite_email']]
              subject = "Mathfeud Invite"
              user_profile = UserProfile.objects.get(user=request.user)
              message = "Active your account at " + request.build_absolute_uri(reverse('member_register')) + "?group_name=" +  user_profile.group.name
              send_mail(subject, message, 'mathfeud@psychstat.org', invite_email, fail_silently=False)
              render(request, 'main/profile.html',{})
         else:
              print form.errors
    else:
        form = InviteForm()
    return render(request, 'main/profile.html', {'form':form})

def getVideos(request):
	return render_to_response('main/videos.html', {'videos': Video.objects.order_by('grade')})

def getVideo(request, vidNumber):
	return render_to_response('main/video.html', {'video': Video.objects.get(id=vidNumber)})
