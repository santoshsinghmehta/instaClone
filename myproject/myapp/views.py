# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import SignUpForm
from models import UserModel
from django.contrib.auth.hashers import make_password

# Create your views here.
def signup_view(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')

    else:
        form = SignUpForm()
    return render(request, 'index.html',{'form':form})
