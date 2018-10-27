from django import forms
from django.utils.translation import gettext_lazy as gettext
from .models import *

class LenderForm(forms.ModelForm):
    class Meta:
        model = Lenders

        fields = (
            'first_name',
            'last_name',
            'company',
            'address',
            'city',
            'state',
            'zip_code',
            'h_email',
            'w_email',
            'h_phone',
            'w_phone',
            'solicitation',
        )
        labels = {
            'first_name': gettext('First Name'),
            'last_name': gettext('Last Name'),
            'zip_code': gettext('Zip'),
            'h_email': gettext('Email (H)'),
            'w_email': gettext('Email (W)'),
            'h_phone': gettext('Phone (H)'),
            'w_phone': gettext('Phone (W)'),
        }

        widgets = {
            
        }


class QualifierForm(forms.Form):
    qualifiers = forms.ModelMultipleChoiceField(
        #queryset = Qualifiers.objects.order_by('name'),
        widget = forms.CheckboxSelectMultiple,
        queryset=None
    )
    #class Meta:
    #    model = Qualifiers

    #    fields = (
    #    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['qualifiers'].queryset = Qualifiers.objects.order_by('name')

