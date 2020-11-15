from django.db import models
import os
import uuid


class UniqueImageField(models.ImageField):
    def generate_filename(self, instance, filename):
        _, ext = os.path.splitext(filename) 
        name = f'{uuid.uuid4().hex}{ext}'
        return super().generate_filename(instance, name)


class User(models.Model):
    genders = (
        ('male', 'male'),
        ('female', 'female'),
    )

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=32, choices=genders, default='male')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = UniqueImageField(upload_to='images', null=True)
    last_active = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['created_at']
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Room(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['updated_at']
        verbose_name = 'room'
        verbose_name_plural = 'rooms'


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['id']
        verbose_name = 'message'
        verbose_name_plural = 'messages'