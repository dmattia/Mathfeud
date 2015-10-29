from registration.backends.default.views import RegistrationView
from forms import UserProfileRegistrationForm
from models import UserProfile, GroupProfile, PendingInvite
from django.contrib.auth.models import Group
from registration.forms import RegistrationFormUniqueEmail

class MyRegistrationView(RegistrationView):
	form_class = UserProfileRegistrationForm
	
	def register(self, request, form_class):
		new_user = super(MyRegistrationView, self).register(request, form_class)
		g = Group.objects.get(name='groupAdmin')
		g.user_set.add(new_user)
		group_profile = GroupProfile.create(name=form_class.cleaned_data['group_name'], school=form_class.cleaned_data['school'])
		user_profile = UserProfile()
		user_profile.user = new_user
		user_profile.group = group_profile
		user_profile.save()

class GroupMemberRegView(RegistrationView):
	form_class = RegistrationFormUniqueEmail

	def register(self, request, form_class):
		new_user = super(GroupMemberRegView, self).register(request, form_class)
		g = Group.objects.get(name='groupMember')
		g.user_set.add(new_user)
		group_activation = request.GET.get('group_name')
		group_profile = PendingInvite.objects.get(activation_key=group_activation).group
		user_profile = UserProfile()
		user_profile.user = new_user
		user_profile.group = group_profile
		user_profile.save()
