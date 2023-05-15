
from django.shortcuts import render, redirect
from .form import CustomUserCreationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
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
            author_group = Group.objects.get(name='author')
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