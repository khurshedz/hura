from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm
import logging

def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    agent = request.META.get('HTTP_USER_AGENT', '')
    print(agent)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            if request.user.is_authenticated:
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)

            else:
                form = PostForm()
                return render(request, 'blog/post_error.html', {'form': form})

    else:
        form = PostForm()
    agent = request.META.get('HTTP_USER_AGENT', '')
    print(agent)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return HttpResponseRedirect("/")
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def contacts(request):
    return render(request, 'blog/contacts.html')

def about(request):
    return render(request, 'blog/about.html')

def unique(request):
    agent = request.META.get('HTTP_USER_AGENT', '')
    print(agent)
    return render(request, 'blog/unique.html')


logger = logging.getLogger(__name__)

def home(request):
    agent = request.META.get('HTTP_USER_AGENT', '')
    print(agent)
    logger.debug('A debug message')

    return render(request, 'blog/about.html')