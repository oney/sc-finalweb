import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password, make_password
from .. import models
from ..forms import LoginForm, RegisterForm, EditForm, PasswordForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from ..jwthelper import jwt_encode, jwt_decode
from ..mailhelper import sendmail


class ChatView(ListView):
    paginate_by = 5
    template_name = 'dating/chats.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        user_id = self.request.session['user_id']
        return models.Room.objects\
            .filter(Q(user1=user_id) | Q(user2=user_id))\
            .order_by('-updated_at')\
            .prefetch_related('user1', 'user2')

    def render_to_response(self, context):
        if not self.request.session.get('is_login', None):
            return redirect("/")
        return super(ChatView, self).render_to_response(context)