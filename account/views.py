
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()
def register(request):
    
    return render('account/register.html')
