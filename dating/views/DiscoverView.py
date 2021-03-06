import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .. import models
from django.views.generic import ListView
from django.db.models import Q


class DiscoverView(ListView):
    '''
    /discover page handler
    '''
    paginate_by = 6
    model = models.User
    template_name = 'dating/discover.html'
    context_object_name = 'users'

    def get_queryset(self):
        '''
        Return model list of the page

        **Returns**

            queryset: *django.db.models.query.QuerySet*
                The QuerySet

        '''
        user_id = self.request.session['user_id']
        # ORDER BY last_active DESC
        return models.User.objects.filter(~Q(id=user_id))\
            .order_by('-last_active')

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
        return super(DiscoverView, self).render_to_response(context)
