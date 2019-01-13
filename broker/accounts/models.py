from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# NOTE: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#extending-the-existing-user-model
class User(AbstractUser):
    address  = models.CharField(max_length=50, default=None, null=True, blank=True)
    city     = models.CharField(max_length=50, default=None, null=True, blank=True)
    state    = models.CharField(max_length=2, default=None, null=True, blank=True)
    zip_code = models.CharField(max_length=10, default=None, null=True, blank=True)
    # NOTE https://github.com/VeryApt/django-phone-field
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phone    = models.CharField(max_length=10, blank=True)

    def __str__(self):
        self.email
