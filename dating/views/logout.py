from django.shortcuts import render, redirect
from django.http import HttpResponse


def logout(request):
    '''
    /logout page handler

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
    # Clear all data in session
    request.session.flush()
    return redirect('/')
