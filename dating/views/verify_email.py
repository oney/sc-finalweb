from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. import models
from ..helpers import jwt_decode


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