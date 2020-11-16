from django.db import models
from .User import User


class Room(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    messages_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['updated_at']
        verbose_name = 'room'
        verbose_name_plural = 'rooms'
