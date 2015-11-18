from django.shortcuts import render
from quiz.models import MultipleChoiceQuestion
from quiz.forms import QuestionForm

# Create your views here.
def all_questions(request):
	choices = (
		('hiya', 'this is option 1'),
		('b', 'b'),
		('c', 'c'),
		('d', 'd'),
	)
	data = {
		'title': 'This is the title',
	}
	form = QuestionForm(initial=data, choices=choices)
	context_dict = {
		'form': form,
	}
	return render(request, 'quiz/questions.html', context_dict)
