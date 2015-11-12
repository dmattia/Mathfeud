from registration.forms import RegistrationFormUniqueEmail
from django import forms
from main.models import *
from django.utils.safestring import mark_safe

class UserProfileRegistrationForm(RegistrationFormUniqueEmail):
	school = forms.CharField()
	group_name = forms.CharField()
	picture = forms.ImageField()

class InviteForm(forms.Form):
	invite_email = forms.EmailField(max_length=128, help_text="sending invitation to the email address")

class GroupProfileForm(forms.ModelForm):
	class Meta:
		model = GroupProfile
		exclude = ["GroupProfile"]

class PlainTextWidget(forms.Widget):
	def render(self, _name, value, _attrs):
		return mark_safe(value)

class GroupReadOnlyForm(GroupProfileForm):
	def __init__(self, *args, **kwargs):
		super(GroupReadOnlyForm, self).__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['disabled'] = 'true'

class UpdateProfilePictureForm(forms.Form):
	newPic = forms.ImageField()
