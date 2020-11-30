from django.db import models
import os
import uuid


class UniqueImageField(models.ImageField):
    '''
    Unique image field
    '''
    def generate_filename(self, instance, filename):
        '''
        generate a unique file name

        **Parameters**

            instance: *<User>*
                User model

            filename: *str*
                The original file name

        **Returns**

            filename: *str*
                Unique file name

        '''
        _, ext = os.path.splitext(filename)
        name = f'{uuid.uuid4().hex}{ext}'  # Unique random string
        return super().generate_filename(instance, name)


class User(models.Model):
    '''
    User model
    '''
    genders = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=32, choices=genders, default='male')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = UniqueImageField(upload_to='images', null=True, blank=True)
    last_active = models.DateTimeField(auto_now_add=True, null=True)
    email_verified = models.BooleanField(default=False)
    picture_violated = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['created_at']
        verbose_name = 'user'
        verbose_name_plural = 'users'
