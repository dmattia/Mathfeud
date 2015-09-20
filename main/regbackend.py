from registration.backends.default.views import RegistrationView
from forms import UserProfileRegistrationForm
from models import UserProfile

class MyRegistrationView(RegistrationView):
	form_class = UserProfileRegistrationForm
	
	def register(self, request, form_class):
		new_user = super(MyRegistrationView, self).register(request, form_class)
		new_group = 
		user_profile = UserProfile()
		user_profile.user = new_user
		user_profile.school = form_class.cleaned_data['school']
		user_profile.save()
