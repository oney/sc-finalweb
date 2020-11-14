from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from . import models
from .forms import LoginForm, RegisterForm

def index(request):
    template = 'index.html'
    context = {}
    return render(request, template, context)

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        form = LoginForm(request.POST)
        message = "Some fields are invalid"
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.email
                    return redirect('/index/')
                else:
                    message = "Password is wrong"
            except:
                message = "User not found"
        return render(request, 'dating/login.html', locals())

    form = LoginForm()
    return render(request, 'dating/login.html', locals())

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        message = "Some fields are invalid"
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            gender = form.cleaned_data['gender']
            if password != confirm_password:
                message = "Confirm password not match"
                return render(request, 'dating/register.html', locals())
            else:
                user = models.User.objects.filter(email=email)
                if user:
                    message = 'Email is already registered'
                    return render(request, 'dating/register.html', locals())

                user = models.User.objects.create()
                user.name = name
                user.password = make_password(password)
                user.email = email
                user.gender = gender
                user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    form = RegisterForm()
    return render(request, 'dating/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')