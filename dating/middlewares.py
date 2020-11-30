from . import models
from django.utils import timezone


class DatingMiddleware:
    '''
    Middleware listens all HTTP requests
    '''
    def __init__(self, get_response):
        '''
        The class initializer

        **Parameters**

            get_response: *function*
                get_response

        '''
        self.get_response = get_response

    def __call__(self, request):
        '''
        **Parameters**

            request: *channels.http.AsgiRequest*
                request

        '''
        response = self.get_response(request)
        # If the client login, update last_active to now
        if request.session.get('is_login', None):
            user = models.User.objects.get(pk=request.session['user_id'])
            if user:
                user.last_active = timezone.now()
                user.save()

        return response
