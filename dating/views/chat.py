import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from django.db.models import Q
from ..helpers import jwt_encode


def chat(request, id):
    '''
    /chat page handler

    **Parameters**

        request: *channels.http.AsgiRequest*
            The request

        id: *int*
            The id of the user to chat

    **Returns**

        response: *django.http.response.HttpResponse*
            The response

    '''
    # If not login, redirect to home
    if not request.session.get('is_login', None):
        return redirect("/")
    me = models.User.objects.get(pk=request.session['user_id'])
    user = models.User.objects.get(pk=id)

    # It's not allowd to chat with self
    if me.id == user.id:
        return redirect("/discover")

    # It's not allowd to chat without email verification
    if not me.email_verified:
        return render(request, 'dating/cant_chat.html', locals())

    # Generate JWT token for communication via websocket
    jwt_token = jwt_encode({
        "user_id": me.id,
        "exp": int(time.time() + 60*60*24*60)
        })

    # Find or create a room with (user1, user2) matching (me, user)
    try:
        room = models.Room.objects\
            .get(Q(user1=me, user2=user) | Q(user2=me, user1=user))
    except models.Room.DoesNotExist:
        room = models.Room.objects.create(user1=me, user2=user)

    messages = room.message_set.all().prefetch_related('user')
    return render(request, 'dating/chat.html', locals())
