from django.shortcuts import render, redirect
from django.http import HttpResponse


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/")
    request.session.flush()
    return redirect('/')
