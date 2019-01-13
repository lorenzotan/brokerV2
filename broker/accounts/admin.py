from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

# inline model admin to add UserProfile to admin
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#extending-the-existing-user-model
admin.site.register(User, UserAdmin)
