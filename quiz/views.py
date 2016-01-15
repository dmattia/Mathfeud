from django.shortcuts import render
from quiz.models import Question, Answer, QuestionResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
import re
from main.models import UserProfile

@login_required
def checkQuestionSubmission(request):
	""" Takes in post data from question form
	Determines if the question was answered correctly
	Adds a "Question Response" row recording this submission

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
				if not answer.correct and user_answer:
					response['Correct'] = 'Incorrect'
					response['Explaination'] = 'The correct answer was not chosen'
		else:
			response['valid-response'] = 'No'
			response['Explaination'] = 'Server Error: Question number could not be determined'
	else:
		response['valid-response'] = 'No'
		response['Correct'] = 'Incorrect'
		response['Explaination'] = 'This page can only be accessed via a POST request'

	recordResponse(request, question, response['Correct'])
	return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def recordResponse(request, question, correct):
	""" Records the question response
	"""
	response = QuestionResponse()
	response.user = UserProfile.objects.get(user=request.user)
	response.question = question
	response.correct = bool(correct == 'Correct')
	response.save()
