from django.shortcuts import get_object_or_404, redirect, render
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
    qualifiers     = Qualifier.objects.order_by('name')
    property_types = PropertyType.objects.order_by('name')

    if req.method == 'POST':
        lenderForm = LenderForm(req.POST)
        #lenderForm.save()

        qualifierForm = QualifierForm(req.POST)
        #qualifierForm.save()
        userForm                   = UserForm(req.POST, instance=req.user)
        lenderForm                 = LenderForm(req.POST)
        lenderOwnerOccupiedREForm  = LenderOwnerOccupiedREForm(req.POST)
        lenderInvestmentREForm     = LenderInvestmentREForm(req.POST)
        lenderMultiFamilyLoanForm  = LenderMultiFamilyLoanForm(req.POST)
        lenderConstructionLoanForm = LenderConstructionLoanForm(req.POST)
        lenderSBALoanForm          = LenderSBALoanForm(req.POST)
        lenderHELOCLoanForm        = LenderHELOCLoanForm(req.POST)
        lenderBLOCLoanForm         = LenderBLOCLoanForm(req.POST)
        lenderBridgeLoanForm       = LenderBridgeLoanForm(req.POST)

        if userForm.is_valid() and \
           lenderForm.is_valid() and \
           lenderOwnerOccupiedREForm.is_valid() and \
           lenderInvestmentREForm.is_valid() and \
           lenderMultiFamilyLoanForm.is_valid() and \
           lenderConstructionLoanForm.is_valid() and \
           lenderSBALoanForm.is_valid() and \
           lenderHELOCLoanForm.is_valid() and \
           lenderBLOCLoanForm.is_valid() and \
           lenderBridgeLoanForm.is_valid():

            user = userForm.save()

            lender = lenderForm.save(commit=False)
            lender.user = user
            lender_id = lender.save()

            oo = lenderOwnerOccupiedREForm.save(commit=False)
            oo.lender = lender_id
            oo.save()

            inv = lenderInvestmentREForm.save(commit=False)
            inv.lender = lender_id
            inv.save()

            multi  = lenderMultiFamilyLoanForm.save(commit=False)
            multi.lender = lender_id
            multi.save()

            const  = lenderConstructionLoanForm.save(commit=False)
            const.lender = lender_id
            const.save()

            sba    = lenderSBALoanForm.save(commit=False)
            sba.lender = lender_id
            sba.save()

            heloc  = lenderHELOCLoanForm.save(commit=False)
            heloc.lender = lender_id
            heloc.save()

            bloc   = lenderBLOCLoanForm.save(commit=False)
            bloc.lender = lender_id
            bloc.save()

            bridge = lenderBridgeLoanForm.save(commit=False)
            bridge.lender = lender_id
            bridge.save()

            return redirect('loans:lenders')

    else:
        user = { 'first_name': req.user.first_name, 'last_name': req.user.last_name }
        userForm                   = UserForm(user)
        lenderForm                 = LenderForm()
        lenderOwnerOccupiedREForm  = LenderOwnerOccupiedREForm()
        lenderInvestmentREForm     = LenderInvestmentREForm()
        lenderMultiFamilyLoanForm  = LenderMultiFamilyLoanForm()
        lenderConstructionLoanForm = LenderConstructionLoanForm()
        lenderSBALoanForm          = LenderSBALoanForm()
        lenderHELOCLoanForm        = LenderHELOCLoanForm()
        lenderBLOCLoanForm         = LenderBLOCLoanForm()
        lenderBridgeLoanForm       = LenderBridgeLoanForm()
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
    templ = loader.get_template('lender/list.html')

    lender_list = Lender.objects.all().select_related('user')
    context = {
        'lenders': lender_list,
    }

    return HttpResponse(templ.render(context, req))


@login_required
@user_passes_test(lambda u: u.groups.filter(name='client').count() == 0, login_url='/denied/')
def lender_detail(req, pk):
    templ = loader.get_template('lender/detail.html')
    lender = get_object_or_404(Lender.objects.select_related('user'), id=pk)
    qs = LenderOwnerOccupiedRE.objects.select_related('lender')
    print (qs.query)
    oo     = get_object_or_404(qs, lender=pk)
    inv    = get_object_or_404(LenderInvestmentRE.objects.select_related('lender'), lender=pk)
    multi  = get_object_or_404(LenderMultiFamilyLoan.objects.select_related('lender'), lender=pk)
    const  = get_object_or_404(LenderConstructionLoan.objects.select_related('lender'), lender=pk)
    sba    = get_object_or_404(LenderSBALoan.objects.select_related('lender'), lender=pk)
    heloc  = get_object_or_404(LenderHELOCLoan.objects.select_related('lender'), lender=pk)
    bloc   = get_object_or_404(LenderBLOCLoan.objects.select_related('lender'), lender=pk)
    bridge = get_object_or_404(LenderBridgeLoan.objects.select_related('lender'), lender=pk)

    context = {
        'lender_data': lender,
        'owner_occupy': oo,
        'invest': inv,
        'multi': multi,
        'const': const,
        'sba': sba,
        'heloc': heloc,
        'bloc': bloc,
        'bridge': bridge,
    }

    return HttpResponse(templ.render(context, req))


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
