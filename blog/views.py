from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
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

def post_search(request):
    if request.method == 'GET':
        title = request.GET['title']
        year = int(request.GET['year'])
        found_articles = []
        for article in articles_list:
            if (name == article[1]) and (year == article[2]):
                found_articles.append(article)
        beautiful_html = generate_html(found_articles)
        return HttpResponse(beautiful_html)
    return render(request, 'blog/post_search.html')


def contacts(request):
    return render(request, 'blog/contacts.html')

def about(request):
    return render(request, 'blog/about.html')

def unique(request):
    return render(request, 'blog/unique.html')
