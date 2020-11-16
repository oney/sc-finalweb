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


def verify_email(request):
    try:
        info = jwt_decode(request.GET.get('token'))
        user = models.User.objects.get(pk=info['user_id'])
        user.email_verified = True
        user.save()
        success = True
    except:
        success = False
    return render(request, 'dating/verify_email.html', locals())