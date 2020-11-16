import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. import models
from django.db.models import Q
from ..jwthelper import jwt_encode


def chat(request, id):
    if not request.session.get('is_login', None):
        return redirect("/")
    me = models.User.objects.get(pk=request.session['user_id'])
    user = models.User.objects.get(pk=id)
    if me.id == user.id:
        return redirect("/discover")
    if not me.email_verified:
        return render(request, 'dating/cant_chat.html', locals())
    jwt_token = jwt_encode({
        "user_id": me.id,
        "exp": int(time.time() + 60*60*24*60)
        })

    try:
        room = models.Room.objects\
            .get(Q(user1=me, user2=user) | Q(user2=me, user1=user))
    except models.Room.DoesNotExist:
        room = models.Room.objects.create(user1=me, user2=user)
    
    messages = room.message_set.all().prefetch_related('user')
    return render(request, 'dating/chat.html', locals())