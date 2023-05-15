from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from datetime import datetime
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

# Create your views here.
import math


def all_posts(request):
    
    blogs = Post.objects.filter(date_published__isnull=False).order_by('-date_published')
    paginator = Paginator(blogs, 2)
    page = request.GET.get('page')
    try:
        # Retrieve the posts for the requested page
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        blogs = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page of results
        blogs = paginator.page(paginator.num_pages)
    for blog in blogs:
        blog.read_time = math.ceil(len(blog.body.split(' '))/264)
        blog.comment_count = Comment.objects.filter(post=blog).count()
    return render(request, 'blog/archive.html', {'blogs': blogs})


def page(request):
    return render(request, 'blog/page.html')

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                post.author = "Anonymous"
            tags=post.tags.split(',')[0:3]
            post.tags =','.join(tags)
            post.date_published = datetime.now()
            post.save()
            return redirect('all_posts')
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    
    if request.method=="POST":
        try:
            reply = request.POST.get('reply', '')
            comment_id = request.POST.get('object_pk', '')
            
        except:
            reply = None
            comment_id = None
        try:
            comment=request.POST.get('comment', '')
        except:
            comment = None
        author = request.user
        date_published = datetime.now()
        
        try:
            upvote = request.POST.get('upvote', '')
            
        except:
            upvote= None
        try:
            downvote = request.POST.get('downvote', '')
        except:
            downvote = None
        if upvote:
            if request.user in post.downvotes:
                post.downvotes.remove(request.user)
            post.upvotes.add(request.user)
            post.save()
        if downvote:
            if request.user in post.upvotes:
                post.upvotes.remove(request.user)
            post.downvotes.add(request.user)
            post.save()
        
        if reply and comment_id :
            replied_comment = get_object_or_404(Comment, id=comment_id)
            Comment.objects.create(text=reply, author=author, date_published=date_published, post=post, reply_comment=replied_comment)
        else:
            if comment:
                Comment.objects.create(text=comment, author=author, date_published=date_published, post=post)

                
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'blog/post.html', {'post': post, 'comments':comments})




