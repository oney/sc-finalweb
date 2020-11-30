import time
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from ..forms import EditForm


dir_path = os.path.dirname(os.path.realpath(__file__))


def check_picture(form, user):
    if 'picture' not in form.changed_data:
        return

    user.refresh_from_db()
    if not user.picture:
        return

    from ..detection import detect

    src = os.path.join(dir_path, "../../media", user.picture.path)
    user.picture_violated = detect(src)
    user.save()


def edit(request):
    if not request.session.get('is_login', None):
        return redirect("/")

    user = models.User.objects.get(pk=request.session['user_id'])
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=user)
        message = "Some fields are invalid"
        if form.is_valid():
            form.save()
            check_picture(form, user)
            message = "Save successfully!"
    else:
        form = EditForm(instance=user)
    return render(request, 'dating/edit.html', locals())
