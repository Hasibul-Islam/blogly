from django.shortcuts import render, redirect
from Blog.models import Newsletter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
def home(request):
    return render(request, 'index.html')
def message_sent(request):
    return render(request, 'newsletter/message_sent_successfully.html')
def contact_us(request):
    if request.method=='POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        subscribe = request.POST.get('subscribe', False)
        if subscribe:
            Newsletter.objects.create(email=email, message=message, subscribe=True)
        else:
            Newsletter.objects.create(email=email, message=message, subscribe=False)
        return redirect('message_sent')
    return render(request, 'contact.html')

def contact_us_messages(request):
    newsletters = Newsletter.objects.all().order_by('-pk')
    paginator = Paginator(newsletters, 5)
    page = request.GET.get('page')
    try:
        # Retrieve the posts for the requested page
        newsletters = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        newsletters = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page of results
        newsletters = paginator.page(paginator.num_pages)
    return render(request, 'newsletter/received_message_list.html', {'newsletters':newsletters})