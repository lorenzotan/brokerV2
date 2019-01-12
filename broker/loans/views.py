from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def lender_form(req):
    if req.method == 'POST':
        form = LenderForm(req.POST)
        form.save()
    else:
        form = LenderForm()

    return render(req, 'loans/lender_form.html', {'form': form})



def lender_list(req):
    template = loader.get_template('loans/lender_list.html')
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

    return render(req, 'loans/loan_form.html', {'form': form})


def loan_list(req):
    template = loader.get_template('loans/loan_list.html')
    loan_list = Lenders.objects.all()
    context = {
        'loans': loan_list,
    }

    return HttpResponse(template.render(context, req))
