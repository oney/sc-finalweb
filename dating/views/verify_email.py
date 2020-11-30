from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from ..helpers import jwt_decode


def verify_email(request):
    '''
    /verify_email page handler

    **Parameters**

        request: *channels.http.AsgiRequest*
            The request

    **Returns**

        response: *django.http.response.HttpResponse*
            The response

    '''
    try:
        info = jwt_decode(request.GET.get('token'))  # encode JWT token
        user = models.User.objects.get(pk=info['user_id'])
        user.email_verified = True  # set email_verified True
        user.save()
        success = True
    except Exception:
        # JWT token is invalid
        success = False
    return render(request, 'dating/verify_email.html', locals())
