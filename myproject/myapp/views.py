# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from time import timezone

from django.shortcuts import render,redirect
from forms import SignUpForm,LoginForm,PostForm,LikeForm
from models import UserModel,SessionToken,PostModel,LikeModel
from django.contrib.auth.hashers import make_password,check_password
from myproject.settings import BASE_DIR
from imgurpython import ImgurClient

YOUR_CLIENT_ID = 'f5119726c4ba0f9'
YOUR_CLIENT_SECRET = '466ab27d37ccc8506b870ea2ad5a6c757738bf9c'

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


def login_view(request):
    dict = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #sql query
            user = UserModel.objects.filter(username=username).first()
            if user:
                if not check_password(password, user.password):
                    dict['messages']='invalid password please try again'
                else:
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
    else:
        form = LoginForm()

    dict['form']=form
    return render(request, 'login.html', dict)





def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + '/' +post.image.url)

                client = ImgurClient(YOUR_CLIENT_ID, YOUR_CLIENT_SECRET)
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')

def feed_view(request):
    user = check_validation(request)
    if user:
            posts = PostModel.objects.all().order_by('created_on')
            return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login')



#For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            #time_to_live = session.created_on + timedelta(day=1)
            if True:
                return session.user
    else:
        return None
