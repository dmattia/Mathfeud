from django import forms

class QuestionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		choices = kwargs.pop('choices', None)
		super(QuestionForm, self).__init__(*args, **kwargs)
		if choices is not None:
			self.fields['picked'].choices = choices
	title = forms.CharField()
	picked = forms.MultipleChoiceField(choices=(('a', 'no options found')))
