from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from qa.models import *
from django.forms import ModelForm
from django.core.context_processors import csrf
from main.models import UserProfile, view_page, UserActivityLog
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def main(request):
	""" main question list """
	view_page(request.user, UserActivityLog.QALIST)
	questions = Question.objects.all().order_by("-created")
	paginator = Paginator(questions, 10)
	activity_logs = UserActivityLog.objects.all().filter(page_viewed = UserActivityLog.QA)	

	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		questions = paginator.page(page)
	except (InvalidPage, EmptyPage):
		questions = paginator.page(paginator.num_pages)
	votes = {}
	views = {}
	for question in questions:
		if (len(question.body) > 500):
			question.body = question.body[:500] + "..."
		#get votes for question
		answers = Answer.objects.all().filter(question = question)
		num_votes = 0
		for a in answers:
			num_votes += a.score
		votes[question.pk] = num_votes
		views[question.pk] = activity_logs.filter(id_viewed = question.pk).count()
	context_dict = {'votes': votes, 'views': views, 'questions':questions, 'user':UserProfile.objects.get(user=request.user)}
	return render(request, 'qa/list.html', context_dict)

class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['body']

@login_required
def add_answer(request, questionpk):
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			newAnswer = Answer()
			newAnswer.poster = UserProfile.objects.get(user=request.user)
			newAnswer.body = form.cleaned_data['body']
			newAnswer.question = Question.objects.get(pk=int(questionpk))
			newAnswer.save()
	return HttpResponseRedirect((reverse("question", args=[questionpk])))


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'body']

@login_required
def NewQuestion(request):
	""" Add new question """
	context_dict = {'form':QuestionForm(), 'user':UserProfile.objects.get(user=request.user)}
	context_dict.update(csrf(request))
	return render(request, "qa/newquestion.html", context_dict)

@login_required
def add_question(request):
	""" Add a new question action """
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			newQuestion = Question()
			newQuestion.body = form.cleaned_data['body']
			newQuestion.title = form.cleaned_data['title']
			
			newQuestion.save()
	return HttpResponseRedirect(reverse("qaList"))

@login_required
def question(request, pk):
	view_page(request.user, UserActivityLog.QA, pk)

	question = Question.objects.get(pk=int(pk))
	answers = Answer.objects.filter(question=question)
	d = {'question':question, 'user':UserProfile.objects.get(user=request.user), 'answers': answers, 'form': AnswerForm()}
	if not question.solved and request.user == question.poster.user:
		d['allowSelect'] = True
	else:
		d['allowSelect'] = False
	return render(request, "qa/question.html", d)

@login_required
def selectBestAnswer(request, answer_id):
	answer = Answer.objects.get(pk = int(answer_id))
	answer.isBestAnswer = True
	question = answer.question
	answer.save()
	
	question.solved = True
	questionpk = question.pk
	question.save()
	#answers = Answer.objects.filter(question = question)
	#d = {'question':question, 'user':UserProfile.objects.get(user=request.user), 'answers': answers, 'form': AnswerForm(), 'allowSelect':False}
	#return render(request, "qa/question.html", d)
	return HttpResponseRedirect((reverse("question", args=[questionpk])))

@login_required
def vote(request):
	"""
	upvote answer pk if up is 1, else downvote pk
	"""
	response_data = {}
	if request.method == 'POST':
		pk = request.POST['answer_id']
		up = request.POST['up']
		answer = Answer.objects.get(pk=int(pk))
		voter = UserProfile.objects.get(user=request.user)
		vote = Votes.objects.filter(voter=voter).filter(answer=answer)
		if len(vote) > 0:
			# already voted
			response_data['valid-response'] = 'No'
                	return HttpResponse(
                        	json.dumps(response_data),
                        	content_type = "application/json"
                	)

		new_score = answer.score
		new_vote = Votes()
                new_vote.voter = voter
                new_vote.answer = answer
		if int(up) == 1:
			new_score += 1
			answer.score = new_score
			new_vote.up = True
		else:
			new_score -= 1
			answer.score = new_score
                        new_vote.up = False
                new_vote.save()
		answer.save()
		response_data['valid-response'] = 'Yes'
		response_data['score'] = new_score
		return HttpResponse(
			json.dumps(response_data),
			content_type = "application/json"
		)
	else:
		response_data['valid-response'] = 'No'
		return HttpResponse(
			json.dumps(response_data),
			content_type = "application/json"
		)
