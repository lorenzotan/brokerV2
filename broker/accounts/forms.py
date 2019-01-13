from django import forms
from django.contrib.auth.models import User
from loans.models import

class RegisterForm(ModelForm):
    class Meta():
        model = User
        fields = ['email', 'username', 'password']


