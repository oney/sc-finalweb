import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from ..forms import EditForm
from ..helpers import send_verify_email


def resent(request):
    if not request.session.get('is_login', None):
        return redirect("/")

    user = models.User.objects.get(pk=request.session['user_id'])
    send_verify_email(user)
    return redirect('/edit/')
