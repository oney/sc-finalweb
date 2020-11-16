import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .. import models
from ..forms import RegisterForm
from django.db.models import Q
from ..jwthelper import jwt_encode
from ..mailhelper import sendmail


def send_verify_email(user):
    link = "http://127.0.0.1:8000/verify_email?token=%s" % (
        jwt_encode({
            "user_id": user.id,
            "exp": int(time.time() + 60*60*24*60)
        })
    )
    text = "Verify your email by opening %s" % link
    html = """\
    <html>
    <head></head>
    <body>
        Verify your email by opening <a href="%s">this link</a>
    </body>
    </html>
    """ % link
    sendmail(user.email, "Verify email", text, html)


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
                send_verify_email(user)

                return redirect('/login/')
        return render(request, 'dating/register.html', locals())
    form = RegisterForm()
    return render(request, 'dating/register.html', locals())