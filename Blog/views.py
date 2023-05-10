from django.shortcuts import render

# Create your views here.
def post(request):
    return render(request, 'blog/post.html')


def all_posts(request):
    return render(request, 'blog/archive.html')


def page(request):
    return render(request, 'blog/page.html')