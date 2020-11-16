from . import models
from django.utils import timezone

class DatingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.session.get('is_login', None):
            user = models.User.objects.get(pk=request.session['user_id'])
            if user:
                user.last_active = timezone.now()
                user.save()

        return response