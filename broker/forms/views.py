from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import *

# Create your views here.
def lender_form(req):
    tmpl = loader.get_template('forms/lender_form.html')
    submit = 'Submit'
    qualifiers = Qualifiers.objects.order_by('name')

    if req.method == 'POST':
        lenderForm = LenderForm(req.POST)
        lenderForm.save()

        qualiferForm = QualifierForm(req.POST)
        qualiferForm.save()
    else:
        lenderForm = LenderForm()
        qualifierForm = QualifierForm()

    print ()
    print ("DEBUG: {}".format(qualifierForm))
    print ("DEBUG: {}".format(type(qualifierForm)))
    print ()

    context = {
        'lenderForm': lenderForm,
        #'qualifiers': qualifiers,
        'qualifiers': qualifierForm,
        'submit': submit,
    }
    #return render(req, 'forms/lender_form.html', context)
    return HttpResponse(tmpl.render(context, req))



def lender_list(req):
    template = loader.get_template('forms/lender_list.html')
    lender_list = Lenders.objects.all()
    context = {
        'lenders': lender_list,
    }

    return HttpResponse(template.render(context, req))


def loan_form(req):
    if req.method == 'POST':
        form = LoanForm(req.POST)
        form.save()
    else:
        form = LoanForm()

    return render(req, 'forms/loan_form.html', {'form': form})


def loan_list(req):
    template = loader.get_template('forms/loan_list.html')
    loan_list = Lenders.objects.all()
    context = {
        'loans': loan_list,
    }

    return HttpResponse(template.render(context, req))
