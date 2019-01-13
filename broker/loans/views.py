from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *

# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='client').count() == 0, login_url='/denied/')
def lender_form(req):
    tmpl = loader.get_template('lender/form.html')
    submit = 'Submit'
    qualifiers = Qualifier.objects.order_by('name')
    property_types = PropertyType.objects.order_by('name')

    if req.method == 'POST':
        lenderForm = LenderForm(req.POST)
        #lenderForm.save()

        qualifierForm = QualifierForm(req.POST)
        #qualifierForm.save()
    else:
        userForm = UserForm()
        lenderForm = LenderForm()
        lenderOwnerOccupiedREForm = LenderOwnerOccupiedREForm()
        lenderInvestmentREForm = LenderInvestmentREForm()
        lenderMultiFamilyLoanForm = LenderMultiFamilyLoanForm()
        lenderConstructionLoanForm = LenderConstructionLoanForm()
        lenderSBALoanForm = LenderSBALoanForm()
        lenderHELOCLoanForm = LenderHELOCLoanForm()
        lenderBLOCLoanForm = LenderBLOCLoanForm()
        lenderBridgeLoanForm = LenderBridgeLoanForm()
        #qualifierForm = QualifierForm()

    #print ()
    #print ("DEBUG: {}".format(qualifierForm))
    #print ("DEBUG: {}".format(type(qualifierForm)))
    #print ()

    context = {
        'userForm': userForm,
        'lenderForm': lenderForm,
        'lenderOwnerOccupiedREForm': lenderOwnerOccupiedREForm,
        'lenderInvestmentREForm': lenderInvestmentREForm,
        'lenderMultiFamilyLoanForm': lenderMultiFamilyLoanForm,
        'lenderConstructionLoanForm': lenderConstructionLoanForm,
        'lenderSBALoanForm': lenderSBALoanForm,
        'lenderHELOCLoanForm': lenderHELOCLoanForm,
        'lenderBLOCLoanForm': lenderBLOCLoanForm,
        'lenderBridgeLoanForm': lenderBridgeLoanForm,
        'qualifiers': qualifiers,
        'property_types': property_types,
        'submit': submit,
    }
    #return render(req, 'loans/lender_form.html', context)
    #return render(req, 'loans/lender_form.html', {'form': form})
    return HttpResponse(tmpl.render(context, req))



@login_required
@user_passes_test(lambda u: u.groups.filter(name='client').count() == 0, login_url='/denied/')
def lender_list(req):
    template = loader.get_template('lender/list.html')
    lender_list = Lender.objects.all()
    context = {
        'lenders': lender_list,
    }

    return HttpResponse(template.render(context, req))


@login_required
@user_passes_test(lambda u: u.groups.filter(name='lender').count() == 0, login_url='/denied/')
def loan_form(req):
    if req.method == 'POST':
        form = LoanForm(req.POST)
        form.save()
    else:
        form = LoanForm()

    return render(req, 'client/form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='lender').count() == 0, login_url='/denied/')
def loan_list(req):
    template = loader.get_template('client/list.html')
    loan_list = Lender.objects.all()
    context = {
        'loans': loan_list,
    }

    return HttpResponse(template.render(context, req))
