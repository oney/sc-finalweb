import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from .. import models
from ..forms import LoginForm, RegisterForm, EditForm, PasswordForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from ..jwthelper import jwt_encode, jwt_decode
from ..mailhelper import sendmail


def edit(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    
    user = models.User.objects.get(pk=request.session['user_id'])
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=user)
        message = "Some fields are invalid"
        if form.is_valid():
            form.save()
            message = "Save successfully!"
    form = EditForm(instance=user)
    return render(request, 'dating/edit.html', locals())