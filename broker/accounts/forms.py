from django import forms
from django.contrib.auth.models import User, Group
#from loans.models import

class RegisterForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['email', 'username', 'password']


class GroupForm(forms.Form):
    user_groups = forms.ModelChoiceField(
        queryset = Group.objects.exclude(name='Admin'),
        empty_label = ('Select One'),
        to_field_name='id'
    )
