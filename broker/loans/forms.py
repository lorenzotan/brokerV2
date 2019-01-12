from django import forms
from django.utils.translation import gettext_lazy as gettext
from .models import *

class LenderForm(forms.ModelForm):
    class Meta:
        model = Lender

        fields = (
            'company',
            'solicit',
        )
            #'first_name',
            #'last_name',
            #'address',
            #'city',
            #'state',
            #'zip_code',
            #'email',
            #'phone',


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
        self.fields['qualifiers'].queryset = Qualifier.objects.order_by('name')

