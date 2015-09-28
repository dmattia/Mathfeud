from django.shortcuts import render
from django.core.mail import send_mail
from main.forms import InviteForm

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def profile(request):
    if request.method == 'POST':
         form = InviteForm(request.POST)
         if form.is_valid():
              invite_email = form['invite_email']
              message = ""
              render(request, 'main/profile.html',{})
         else:
              print form.errors
    else:
        form = InviteForm()
    return render(request, 'main/profile.html', {'form':form})
