from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. import models
from django.views.generic.detail import DetailView


class UserView(DetailView):
    model = models.User
    template_name = 'dating/user.html'
    context_object_name = 'user'

    def render_to_response(self, context):
        if not self.request.session.get('is_login', None):
            return redirect("/")
        return super(UserView, self).render_to_response(context)

    def get_object(self, **kwargs):
        print(kwargs)
        return models.User.objects.get(id=self.kwargs['id'])