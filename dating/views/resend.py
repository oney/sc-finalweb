import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from ..forms import EditForm
from ..helpers import send_verify_email


def resend(request):
    '''
    /resend page handler

    **Parameters**

        request: *channels.http.AsgiRequest*
            The request

    **Returns**

        response: *django.http.response.HttpResponse*
            The response

    '''
    # If not login, redirect to home
    if not request.session.get('is_login', None):
        return redirect("/")

    user = models.User.objects.get(pk=request.session['user_id'])
    try:
        send_verify_email(user)  # send verification email
        message = "Succeeded to resend verification email"
    except Exception:
        message = "Failed to resend verification email"
    return render(request, 'dating/resend.html', locals())
