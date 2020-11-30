import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .. import models
from ..forms import RegisterForm
from ..helpers import send_verify_email


def register(request):
    '''
    /register page handler

    **Parameters**

        request: *channels.http.AsgiRequest*
            The request

    **Returns**

        response: *django.http.response.HttpResponse*
            The response

    '''
    # If login, redirect to home
    if request.session.get('is_login', None):
        return redirect('/')

    # Submit register form
    if request.method == "POST":
        form = RegisterForm(request.POST)
        message = "Some fields are invalid"
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            gender = form.cleaned_data['gender']
            # password has to match confirm_password in the form
            if password != confirm_password:
                message = "Confirm password not match"
                return render(request, 'dating/register.html', locals())
            else:
                user = models.User.objects.filter(email=email)
                # check if the email has been used
                if user:
                    message = 'Email is already registered'
                    return render(request, 'dating/register.html', locals())

                user = models.User.objects.create()
                user.name = name
                user.password = make_password(password)  # encrypt password
                user.email = email
                user.gender = gender
                user.save()
                send_verify_email(user)  # send verification email

                return redirect('/login/')
        return render(request, 'dating/register.html', locals())
    form = RegisterForm()
    return render(request, 'dating/register.html', locals())
