from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from qa.models import *
from django.forms import ModelForm
from django.core.context_processors import csrf
from main.models import UserProfile
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def main(request):
	""" main question list """
	questions = Question.objects.all().order_by("-created")
	paginator = Paginator(questions, 10)

	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		questions = paginator.page(page)
	except (InvalidPage, EmptyPage):
		questions = paginator.page(paginator.num_pages)
	for question in questions:
		if (len(question.body) > 500):
			question.body = question.body[:500] + "..."
	context_dict = {'questions':questions, 'user':UserProfile.objects.get(user=request.user)}
	return render(request, 'qa/list.html', context_dict)

class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['body']

def add_answer(request, questionpk):
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			newAnswer = Answer()
			newAnswer.poster = request.user
			newAnswer.body = form.cleaned_data['body']
			newAnswer.question = Question.objects.get(pk=int(questionpk))
			newAnswer.save()
	return HttpResponseRedirect((reverse("question", args=[question.pk])))


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'body']

def NewQuestion(request):
	""" Add new question """
	context_dict = {'form':QuestionForm(), 'user':UserProfile.objects.get(user=request.user)}
	context_dict.update(csrf(request))
	return render(request, "qa/newquestion.html", context_dict)

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

def question(request, pk):
	question = Question.objects.get(pk=int(pk))
	answers = Answer.objects.filter(question=question)
	d = {'question':question, 'user':UserProfile.objects.get(user=request.user), 'answers': answers, 'form': AnswerForm()}
	return render(request, "qa/question.html", d)
