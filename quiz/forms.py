from django import forms

class QuestionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		choices = kwargs.pop('choices', None)
		title = kwargs.pop('title', None)
		super(QuestionForm, self).__init__(*args, **kwargs)
		if choices is not None:
			self.fields['picked'].choices = choices
		self.fields['picked'].widget.attrs['class'] = 'span12'
		self.fields['picked'].label = title

	picked = forms.MultipleChoiceField(label="", choices=(('a', 'no options found')))
