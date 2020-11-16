import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. import models
from ..forms import EditForm


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