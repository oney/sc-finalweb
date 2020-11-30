from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .. import models
from ..forms import PasswordForm


def password(request):
    if not request.session.get('is_login', None):
        return redirect("/")

    if request.method == "POST":
        form = PasswordForm(request.POST)
        message = "Some fields are invalid"
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                message = "Confirm password not match"
                return render(request, 'dating/password.html', locals())
            else:
                user = models.User.objects.get(pk=request.session['user_id'])

                user.password = make_password(password)
                user.save()
                message = "Change password successfully!"
        return render(request, 'dating/password.html', locals())
    form = PasswordForm()
    return render(request, 'dating/password.html', locals())
