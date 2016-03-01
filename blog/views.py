from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from main.models import UserProfile, UserActivityLog, view_page
from django import forms
from ckeditor.widgets import CKEditorWidget
import datetime
from django.contrib.auth.decorators import login_required

from blog.models import *
# Create your views here.

@login_required
def main(request):
    """ Main listing"""
    view_page(request.user, UserActivityLog.BLOG_LIST)	
    current_group = UserProfile.objects.get(user=request.user).group
    posts = Post.objects.all().filter(group=current_group).order_by("-created")
    paginator = Paginator(posts, 10)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)
    for post in posts:
	if (len(post.body) > 500):
		post.body = post.body[:500] + "..."
    context_dict = {'posts':posts, 'user':request.user}
    return render(request, 'blog/list.html', context_dict)

@login_required
def post(request, pk):
    view_page(request.user, UserActivityLog.BLOG, pk)

    post = Post.objects.get(pk=int(pk))
    d = {'post':post, 'user':request.user}
    return render(request, 'blog/post.html', d)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
	fields = ['body']

@login_required
def add_comment(request, postID):
	""" Add a new comment. """
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			newComment = Comment()
			newComment.poster = request.user
			newComment.group = UserProfile.objects.get(user=request.user).group
			newComment.post = Post.objects.get(id=postID)
			newComment.body = form.cleaned_data['body']
			newComment.save()
	return HttpResponseRedirect(reverse("post", args=[postID]))

@login_required
def post(request, pk):
    """ Single post with comments and a comment form """
    view_page(request.user, UserActivityLog.BLOG, pk)

    post = Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    context_dic = {'post':post, 'comments':comments, 'form':CommentForm(), 'user':request.user}
    context_dic.update(csrf(request))
    return render(request, "blog/post.html", context_dic)

class PostForm(ModelForm):
    class Meta:
        model = Post
	fields = ['title', 'body']

@login_required
def add_post(request):
    """ Add a new blog. """
    if request.method == 'POST':
	form = PostForm(request.POST)
	if form.is_valid():
		newPost = Post()
		newPost.body = form.cleaned_data['body']	
		newPost.title = form.cleaned_data['title']
		newPost.poster = request.user
		newPost.group = UserProfile.objects.get(user=request.user).group
		newPost.save()
    return HttpResponseRedirect(reverse("blogList"))

@login_required
def NewPost(request):
    """ Add new post """
    context_dic = {'form':PostForm(), 'user':request.user}
    context_dic.update(csrf(request))
    return render(request, "blog/newpost.html", context_dic)
