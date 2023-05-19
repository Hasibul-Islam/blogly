from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .form import CustomUserCreationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
import random
from django.contrib import messages
import threading
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import ProfileForm
from django.core.mail import EmailMultiAlternatives
from .models import Profile
from django.contrib.sessions import serializers
from django.conf import settings
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form.errors)
        print(form.cleaned_data.get('email'))
        if form.is_valid():
            print('yes')
            # Set the username to be the email address
            form.instance.username = form.cleaned_data.get('email')
            user = form.save()
            author_group = Group.objects.get(name='Author')
            author_group.user_set.add(user)
            # Log the user in
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                print('yes')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid email or password.')
        else:
            form = LoginForm()

        return render(request, 'account/login.html', {'form': form})
    else:
        return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_admin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form.errors)
        print(form.cleaned_data.get('email'))
        if form.is_valid():
            
            # Set the username to be the email address
            form.instance.username = form.cleaned_data.get('email')
            user = form.save()
            admin_group = Group.objects.get(name='Admin')
            print(admin_group)
            admin_group.user_set.add(user)
            # Log the user in
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)


def generate_otp():
    """Generate a random 6-digit OTP."""
    return str(random.randint(100000, 999999))



def send_otp(subject, text_content, html_content, from_email, to):
    def send_email():
        time.sleep(5)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    threading.Thread(target=send_email).start()
def change_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect('change_password')
        user = authenticate(request, username=email, password=password)
        if user is None:
            
            messages.error(request, "Wrong Password or Email")
            return redirect('change_password')
        
        subject = "Your OTP is"  
        # Generate a new OTP and send it to the user's email
        new_otp = generate_otp()
        subject = "Your OTP is "+str(new_otp)
        text_content = "Your OTP is "+str(new_otp)+'. Submit this OTP to change your password.'
        html_content = "<p><strong>"+text_content+"</strong></p>"
        from_email= settings.EMAIL_HOST_USER
        send_otp(subject, text_content, html_content, from_email, [email])
        request.session['otp'] = str(new_otp)
        return redirect('update_password')
        

    return render(request, 'account/change_password.html')

@login_required
def update_password(request):
    otp = request.session.get('otp')
    
    if request.method=="POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('repeat_password')
        submitted_otp = request.POST.get('otp')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('update_password')

        if otp!=submitted_otp:
            messages.error(request, "OTP do not match.")
            return redirect('update_password')
        user = request.user
        user.set_password(new_password)
        user.save()
        login(request, user)
        return redirect('password_changed_successfully')
    return render(request, 'account/submit_password.html')        

def password_changed_successfully(request):
    return render(request, 'account/password_changed_successfully.html')

@login_required
def profile(request):
    user = request.user
    
    profile = user.profile if hasattr(user, 'profile') else None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile, user=user)

    return render(request, 'account/profile.html', {'form': form})
@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        return redirect('profile-create')
    return render(request, 'account/profile-view.html', {'profile': profile})