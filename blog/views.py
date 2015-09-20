from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from blog.models import *
# Create your views here.

def main(request):
    """ Main listing"""
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)
    
    context_dict = {'posts':posts, 'user':request.user}
    return render(request, 'blog/list.html', context_dict)

def post(request, pk):
    """ Single post with comments and a comment form """
    post = Post.objects.get(pk=int(pk))
    d = {'post':post, 'user':request.user}
    return render(request, 'blog/post.html', d)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]

def add_comment(request, pk):
    """ Add a new comment. """
    p = request.POST

    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]: author = p["author"]

        comment = Comment(post=Post.objects.get(pk=pk))
        cf = CommentForm(p, instance=comment)
        cf.fields["author"].required = False

        comment = cf.save(commit=False)
        comment.author = author
        comment.save()
    return HttpResponseRedirect(reverse("post", args=[pk]))

def post(request, pk):
    """ Single post with comments and a comment form """
    post = Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    context_dic = {'post':post, 'comments':comments, 'form':CommentForm(), 'user':request.user}
    context_dic.update(csrf(request))
    return render(request, "blog/post.html", context_dic)
