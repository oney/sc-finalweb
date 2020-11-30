from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from .. import models
from ..forms import LoginForm


def login(request):
    if request.session.get('is_login', None):
        return redirect('/')

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
                    return redirect('/')
                else:
                    message = "Password is wrong"
            except Exception:
                message = "User not found"
        return render(request, 'dating/login.html', locals())

    form = LoginForm()
    return render(request, 'dating/login.html', locals())
