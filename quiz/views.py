from django.shortcuts import render
from quiz.models import MultipleChoiceQuestion
from quiz.forms import QuestionForm
import uuid

# Create your views here.
def view_question(request, questionNumber):
	question = MultipleChoiceQuestion.objects.get(id=questionNumber)
	choices = (
		(1, question.option1),
		(2, question.option2),
		(3, question.option3),
		(4, question.option4)
	)
	result_str = "Not yet answered"
	if request.method == 'POST':
		form = QuestionForm(request.POST, title=question.question, choices=choices)
		if form.is_valid():
			clicked = int(form.cleaned_data['picked'][0].encode('ascii'))
			if question.answer == clicked:
				result_str = 'correct'
			else:
				result_str = 'incorrect'
	else:
		form = QuestionForm(title=question.question, choices=choices)
	context_dict = {
		'form': form,
		'result': result_str,
	}
	return render(request, 'quiz/questions.html', context_dict)
