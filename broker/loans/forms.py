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
            'email_x',
            'phone_w',
            'phone_m',
            'phone_f',
            'phone_o',
        )
        labels = {
            'email':   gettext('Primary Email'),
            'email_x': gettext('Secondary Email'),
            'phone_w': gettext('Work Phone'),
            'phone_m': gettext('Mobile Phone'),
            'phone_f': gettext('Fax Phone'),
            'phone_o': gettext('Other Phone'),
        }


class LenderForm(forms.ModelForm):
    class Meta:
        model = Lender

        fields = (
            'company',
            'lendertype',
            'loanamt',
        )
        labels = {
            'lendertype': gettext('Lender Type'),
            'loanamt': gettext('Loan Amount'),
        }


class LenderBrokerRelationForm(forms.ModelForm):
    class Meta:
        model = LenderBrokerRelation
        solicit = forms.CharField(required=False, widget=forms.TextInput(attrs={'type':'number'}))

        fields  = (
            'solicit',
            'pays_brkr_fees',
            'pays_brkr_rebate',
            'pays_1099',
            'pays_escrow',
        )
        labels = {
            'solicit':          gettext('Solicitation Period'),
            'pays_brkr_fees':   gettext('Pays Broker Fees'),
            'pays_brkr_rebate': gettext('Pays Broker Rebate'),
            'pays_1099':        gettext('Pays via 1099'),
            'pays_escrow':      gettext('Pays through Escrow'),
        }


class LenderOwnerOccupiedREForm(forms.ModelForm):
    class Meta:
        model = LenderOwnerOccupiedRE
        fields = (
            'office',
            'warehouse',
            'manufacturing',
            'medical',
            'mixed_use',
            'industrial',
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
            'industrial',
            'other',
        )


class LenderMultiFamilyLoanForm(forms.ModelForm):
    class Meta:
        model = LenderMultiFamilyLoan
        fields = (
            'mf_2to4',
            'mf_gt4'
        )

        labels = {
            'mf_2to4': gettext('2-4 Units'),
            'mf_gt4':  gettext('4+ Units'),
        }


class LenderConstructionLoanForm(forms.ModelForm):
    class Meta:
        model = LenderConstructionLoan
        fields = (
            'renovation',
            'ground_up_spec',
            'commercial',
            'residential',
            'inv_w_land',
            'oo_w_land',
            'investor'
        )

        labels = {
            'inv_w_land': gettext('Investment w/ Land'),
            'oo_w_land':  gettext('Owner Occupied w/ Land'),
        }


class LenderSBALoanForm(forms.ModelForm):
    class Meta:
        model = LenderSBALoan
        fields = (
            'sba_7a',
            'sba_504',
            'CAPline',
            'micro',
            'express',
            'itl',
            'other'
        )

        labels = {
            'sba_7a':  gettext('7a'),
            'sba_504': gettext('504'),
            'micro':   gettext('Micro Loan'),
            'express': gettext('SBA Express'),
            'itl':     gettext('ITL'),
        }


class LenderHELOCLoanForm(forms.ModelForm):
    class Meta:
        model = LenderHELOCLoan
        fields = (
            'pos_1',
            'pos_2',
            'pos_3'
        )
        labels = {
            'pos_1': gettext('1st Position'),
            'pos_2': gettext('2nd Position'),
            'pos_3': gettext('3rd Position'),
        }


class LenderBLOCLoanForm(forms.ModelForm):
    class Meta:
        model = LenderBLOCLoan
        fields = (
            'resid_prop',
            'stocks',
            'savings',
            'inv_prop',
            'pos1',
            'pos2',
            'equipment',
            'work_cap',
            'int_only',
            'sec_accts_rec',
            'sec_inv',
            're_secure',
            're_unsecure',
        )

        labels = {
            'resid_prop':    gettext('Residential Property'),
            'inv_prop':      gettext('Investment Property'),
            'pos1':          gettext('1st Position'),
            'pos2':          gettext('2nd Position'),
            'equipment':     gettext('Equipment'),
            'work_cap':      gettext('Working Capital'),
            'int_only':      gettext('Interest Only'),
            'sec_accts_rec': gettext('Secured by Accounts Receivable'),
            'sec_inv':       gettext('Secured by Inventory'),
            're_secure':     gettext('RE Secured'),
            're_unsecure':   gettext('RE Unsecured'),
        }


# Misc Loans
class LenderBridgeLoanForm(forms.ModelForm):
    class Meta:
        model = LenderBridgeLoan
        fields = (
            'bridge',
            'comm_term',
            'usda',
            'stated_inc',
        )

        labels = {
            'bridge':     gettext('Bridge Loan'),
            'comm_term':  gettext('Commercial Term Loan'),
            'usda':       gettext('USDA'),
            'stated_inc': gettext('Stated Income'),
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
        self.fields['qualifiers'].queryset = Qualifier.objects.order_by('name')


class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = (
            'company',
        )
