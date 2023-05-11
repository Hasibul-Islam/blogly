from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from datetime import datetime
from .models import Post
# Create your views here.



def all_posts(request):
    return render(request, 'blog/archive.html')


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
    return render(request, 'blog/post.html', {'post': post})