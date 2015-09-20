from registration.forms import RegistrationFormUniqueEmail
from django import forms

class UserProfileRegistrationForm(RegistrationFormUniqueEmail):
	school = forms.CharField()
