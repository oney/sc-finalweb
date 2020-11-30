from django.shortcuts import render,redirect
from django.http import HttpResponse


def index(request):
    '''
    / page handler

    **Parameters**

        request: *channels.http.AsgiRequest*
            The request

    **Returns**

        response: *django.http.response.HttpResponse*
            The response

    '''
    return render(request, 'dating/index.html')
