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
            lender.save()


            # TODO needs to be more efficient
            oo = lenderOwnerOccupiedREForm.save(commit=False)
            oo.lender = lender
            oo.save()

            inv = lenderInvestmentREForm.save(commit=False)
            inv.lender = lender
            inv.save()

            multi  = lenderMultiFamilyLoanForm.save(commit=False)
            multi.lender = lender
            multi.save()

            const  = lenderConstructionLoanForm.save(commit=False)
            const.lender = lender
            const.save()

            sba    = lenderSBALoanForm.save(commit=False)
            sba.lender = lender
            sba.save()

            heloc  = lenderHELOCLoanForm.save(commit=False)
            heloc.lender = lender
            heloc.save()

            bloc   = lenderBLOCLoanForm.save(commit=False)
            bloc.lender = lender
            bloc.save()

            bridge = lenderBridgeLoanForm.save(commit=False)
            bridge.lender = lender
            bridge.save()

            for q in req.POST.getlist('qualifier'):
                lender.qualifiers.add(q)

            for p in req.POST.getlist('property_type'):
                lender.propertytypes.add(p)

            lenderForm.save_m2m()

            return redirect('loans:lenders')

    else:
    # TODO check if lender info exists and prepopulate everything 
        user = { 'first_name': req.user.first_name, 'last_name': req.user.last_name, 'email': req.user.email }
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
# END def lender_form



@login_required
@user_passes_test(lambda u: u.groups.filter(name='client').count() == 0, login_url='/denied/')
def edit_lender_form(req, pk):
    tmpl           = loader.get_template('lender/form.html')
    qualifiers     = Qualifier.objects.order_by('name')
    property_types = PropertyType.objects.order_by('name')
    submit         = 'Update'

    user   = get_object_or_404(User, id=req.user.id)
    lender = get_object_or_404(Lender, id=pk)

    # TODO refactor (create function that returns dictionary of objects)
    try:
        oore = LenderOwnerOccupiedRE.objects.get(lender=pk)
    except LenderOwnerOccupiedRE.DoesNotExist:
        oore = None

    try:
        invre = LenderInvestmentRE.objects.get(lender=pk)
    except LenderInvestmentRE.DoesNotExist:
        invre = None

    try:
        multifam = LenderMultiFamilyLoan.objects.get(lender=pk)
    except LenderMultiFamilyLoan.DoesNotExist:
        multifam = None

    try:
        const = LenderConstructionLoan.objects.get(lender=pk)
    except LenderConstructionLoan.DoesNotExist:
        const = None

    try:
        sba = LenderSBALoan.objects.get(lender=pk)
    except LenderSBALoan.DoesNotExist:
        sba = None

    try:
        heloc = LenderHELOCLoan.objects.get(lender=pk)
    except LenderHELOCLoan.DoesNotExist:
        heloc = None

    try:
        bloc = LenderBLOCLoan.objects.get(lender=pk)
    except LenderBLOCLoan.DoesNotExist:
        bloc = None

    try:
        bridge = LenderBridgeLoan.objects.get(lender=pk)
    except LenderBridgeLoan.DoesNotExist:
        bridge = None

    if req.method == 'POST':
        userForm                   = UserForm(req.POST, instance=user)
        lenderForm                 = LenderForm(req.POST, instance=lender)
        lenderOwnerOccupiedREForm  = LenderOwnerOccupiedREForm(req.POST, instance=oore)
        lenderInvestmentREForm     = LenderInvestmentREForm(req.POST, instance=invre)
        lenderMultiFamilyLoanForm  = LenderMultiFamilyLoanForm(req.POST, instance=multifam)
        lenderConstructionLoanForm = LenderConstructionLoanForm(req.POST, instance=const)
        lenderSBALoanForm          = LenderSBALoanForm(req.POST, instance=sba)
        lenderHELOCLoanForm        = LenderHELOCLoanForm(req.POST, instance=heloc)
        lenderBLOCLoanForm         = LenderBLOCLoanForm(req.POST, instance=bloc)
        lenderBridgeLoanForm       = LenderBridgeLoanForm(req.POST, instance=bridge)

        # TODO refactor: create function to check all necessary forms
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

            # XXX UNIQUE constraint failed: loans_lender.user_id
            user = userForm.save()

            lender = lenderForm.save(commit=False)
            lender.user = user
            lender.save()


            # TODO needs to be more efficient
            oo = lenderOwnerOccupiedREForm.save(commit=False)
            oo.lender = lender
            oo.save()

            inv = lenderInvestmentREForm.save(commit=False)
            inv.lender = lender
            inv.save()

            multi = lenderMultiFamilyLoanForm.save(commit=False)
            multi.lender = lender
            multi.save()

            const = lenderConstructionLoanForm.save(commit=False)
            const.lender = lender
            const.save()

            sba = lenderSBALoanForm.save(commit=False)
            sba.lender = lender
            sba.save()

            heloc = lenderHELOCLoanForm.save(commit=False)
            heloc.lender = lender
            heloc.save()

            bloc = lenderBLOCLoanForm.save(commit=False)
            bloc.lender = lender
            bloc.save()

            bridge = lenderBridgeLoanForm.save(commit=False)
            bridge.lender = lender
            bridge.save()

            for q in req.POST.getlist('qualifier'):
                lender.qualifiers.add(q)

            for p in req.POST.getlist('property_type'):
                lender.propertytypes.add(p)

            lenderForm.save_m2m()

            return redirect('loans:lender_detail', pk=lender.id)

    else:
        userForm                   = UserForm(instance=user)
        lenderForm                 = LenderForm(instance=lender)
        lenderOwnerOccupiedREForm  = LenderOwnerOccupiedREForm(instance=oore)
        lenderInvestmentREForm     = LenderInvestmentREForm(instance=invre)
        lenderMultiFamilyLoanForm  = LenderMultiFamilyLoanForm(instance=multifam)
        lenderConstructionLoanForm = LenderConstructionLoanForm(instance=const)
        lenderSBALoanForm          = LenderSBALoanForm(instance=sba)
        lenderHELOCLoanForm        = LenderHELOCLoanForm(instance=heloc)
        lenderBLOCLoanForm         = LenderBLOCLoanForm(instance=bloc)
        lenderBridgeLoanForm       = LenderBridgeLoanForm(instance=bridge)
        selected_qualifiers        = Lender.objects.values_list('qualifiers__id', flat=True).filter(id=pk)
        selected_propertytypes     = Lender.objects.values_list('propertytypes__id', flat=True).filter(id=pk)


    context = {
        'lender': lender,
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
        'selected_qualifiers': selected_qualifiers,
        'selected_propertytypes': selected_propertytypes,
        'submit': submit,
    }

    return HttpResponse(tmpl.render(context, req))
# END def edit_lender_form


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

    # TODO this needs to be more efficient
    # https://stackoverflow.com/questions/4353147/whats-the-best-way-to-handle-djangos-objects-get
    try:
        oo = LenderOwnerOccupiedRE.objects.get(lender=pk)
    except LenderOwnerOccupiedRE.DoesNotExist:
        oo = None

    try:
        inv = LenderInvestmentRE.objects.get(lender=pk)
    except LenderInvestmentRE.DoesNotExist:
        inv = None

    try:
        multi = LenderMultiFamilyLoan.objects.get(lender=pk)
    except LenderMultiFamilyLoan.DoesNotExist:
        multi = None

    try:
        const = LenderConstructionLoan.objects.get(lender=pk)
    except LenderConstructionLoan.DoesNotExist:
        const = None

    try:
        sba = LenderSBALoan.objects.get(lender=pk)
    except LenderSBALoan.DoesNotExist:
        sba = None

    try:
        heloc = LenderHELOCLoan.objects.get(lender=pk)
    except LenderHELOCLoan.DoesNotExist:
        heloc = None

    try:
        bloc = LenderBLOCLoan.objects.get(lender=pk)
    except LenderBLOCLoan.DoesNotExist:
        bloc = None

    try:
        bridge = LenderBridgeLoan.objects.get(lender=pk)
    except LenderBridgeLoan.DoesNotExist:
        bridge = None

    # https://hackernoon.com/all-you-need-to-know-about-prefetching-in-django-f9068ebe1e60
    # https://docs.djangoproject.com/en/2.0/topics/db/examples/many_to_many/
    quals = lender.qualifiers.all()
    props = lender.propertytypes.all()

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
        'quals': quals,
        'props': props,
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
