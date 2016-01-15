from django.shortcuts import render
from quiz.models import Question, Answer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
import re

@login_required
def checkQuestionSubmission(request):
	""" Takes in post data from question form
	Determines if the question was answered correctly
	Returns:
		HttpResponse containing application/json data from @response
		@response: dictionary on if the answer was correct with a possible explaination
	"""
	response = {
		'valid-response': 'Yes',
		'Correct': 'Correct',
		'Explaination': ''
	}
	if request.method == 'POST' and request.POST:
		questionNumber_str = request.POST['questionNumber']
		questionNumber = int(re.search(r'\d+', questionNumber_str).group())
		if questionNumber:
			question = Question.objects.get(id=questionNumber)
			answers_from_db = Answer.objects.filter(question_ref=question)
			for answer in answers_from_db:
				user_answer = request.POST.get('answer' + str(answer.id), '')
				if answer.correct and user_answer != 'on':
					response['Correct'] = 'Incorrect'
					response['Explaination'] = 'The correct answer was not chosen'
					return HttpResponse(json.dumps(response), content_type="application/json")
				if not answer.correct and user_answer:
					response['Correct'] = 'Incorrect'
					response['Explaination'] = 'The correct answer was not chosen'
					return HttpResponse(json.dumps(response), content_type="application/json")
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			response['valid-response'] = 'No'
			response['Explaination'] = 'Server Error: Question number could not be determined'
			return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		response['valid-response'] = 'No'
		response['Correct'] = 'Incorrect'
		response['Explaination'] = 'This page can only be accessed via a POST request'
		return HttpResponse(json.dumps(response), content_type="application/json")
