from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from django.views.generic.detail import DetailView


class UserView(DetailView):
    '''
    /user page class
    '''
    model = models.User
    template_name = 'dating/user.html'
    context_object_name = 'user'

    def render_to_response(self, context):
        '''
        The renderer

        **Parameters**

            context: *dict*
                Contain info to render

        **Returns**

            response: *django.template.response.TemplateResponse*
                The response

        '''
        # If not login, redirect to home
        if not self.request.session.get('is_login', None):
            return redirect("/")
        return super(UserView, self).render_to_response(context)

    def get_object(self, **kwargs):
        '''
        Return User instance by id parameter

        **Returns**

            user: *dating.models.User.User*
                The user

        '''
        return models.User.objects.get(id=self.kwargs['id'])
