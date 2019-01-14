from django import forms
from django.utils.translation import gettext_lazy as gettext
from .models import *
from accounts.models import User


#-------------------------------------------------------------------------------
# LENDER FORM SECTIONS
#-------------------------------------------------------------------------------
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'address',
            'city',
            'state',
            'zip_code',
            'email',
            'phone',
        )


class LenderForm(forms.ModelForm):
    class Meta:
        model = Lender

        fields = (
            'company',
            'solicit',
        )


class LenderOwnerOccupiedREForm(forms.ModelForm):
    class Meta:
        model = LenderOwnerOccupiedRE
        fields = (
            'office',
            'warehouse',
            'manufacturing',
            'medical',
            'mixed_use',
            'other',
        )


class LenderInvestmentREForm(forms.ModelForm):
    class Meta:
        model = LenderInvestmentRE
        fields = (
            'office',
            'warehouse',
            'manufacturing',
            'medical',
            'mixed_use',
            'other',
        )


class LenderMultiFamilyLoanForm(forms.ModelForm):
    class Meta:
        model = LenderMultiFamilyLoan
        fields = (
            'mf_2to4',
            'mf_gt4'
        )


class LenderConstructionLoanForm(forms.ModelForm):
    class Meta:
        model = LenderConstructionLoan
        fields = (
            'renovation',
            'ground_up_spec',
            'commercial',
            'residential',
            'inv_w_land',
            'oo_w_land'
        )


class LenderSBALoanForm(forms.ModelForm):
    class Meta:
        model = LenderSBALoan
        fields = (
            'sba_7a',
            'sba_504',
            'CAPline',
            'micro',
            'other'
        )


class LenderHELOCLoanForm(forms.ModelForm):
    class Meta:
        model = LenderHELOCLoan
        fields = (
            'pos_1',
            'pos_2'
        )


class LenderBLOCLoanForm(forms.ModelForm):
    class Meta:
        model = LenderBLOCLoan
        fields = (
            'resid_prop',
            'stocks',
            'savings',
            'inv_prop',
            'pos1',
            'pos2'
        )


class LenderBridgeLoanForm(forms.ModelForm):
    class Meta:
        model = LenderBridgeLoan
        fields = (
            'bridge',
        )


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

