from django.db import models
from .User import User
from .Room import Room


class Message(models.Model):
    '''
    Message model
    '''
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%d: %s" % (self.id, self.content)

    class Meta:
        ordering = ['id']
        verbose_name = 'message'
        verbose_name_plural = 'messages'
