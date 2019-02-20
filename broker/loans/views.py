from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from .forms import *

# Create your views here.

################################################################################
# LENDER VIEWS
################################################################################

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Client').count() == 0, login_url='/denied/')
def lender_form(req):
    tmpl = loader.get_template('lender/form.html')
    submit = 'Submit'
    qualifiers     = Qualifier.objects.order_by('name')
    property_types = PropertyType.objects.order_by('name')

    if req.method == 'POST':
        # if the req.user is a Lender
        if req.user.groups.all()[0].name == 'Lender':
            userForm = UserForm(req.POST, instance=req.user)
        # create new user if req.user is broker/admin
        else:
            default_password = 'changeM3!'
            # default user name is first initial, last name
            default_username = (req.POST['first_name'][0] + req.POST['last_name']).lower()
            group = Group.objects.get(name='Lender')

            # TODO check if username exists, if exists, append 01
            new_user = User.objects.create_user(default_username, req.POST['email'], default_password)
            new_user.groups.add(group)
            new_user.save()
            userForm = UserForm(req.POST, instance=new_user)


        lenderForm                 = LenderForm(req.POST)
        lenderBrokerRelationForm   = LenderBrokerRelationForm(req.POST)
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
           lenderBrokerRelationForm.is_valid() and \
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

            # if req.user is a Broker, set new lender to broker
            try:
                lender.broker = req.user.broker
            except ObjectDoesNotExist:
                lender.broker = None

            lender.save()


            # TODO needs to be more efficient
            brkr_rel = lenderBrokerRelationForm.save(commit=False)
            brkr_rel.lender = lender
            brkr_rel.save()

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

    # XXX BEWARE if form is invalid, it will break
    else:
        # Only Broker/Admin can create new lenders
        if req.user.groups.all()[0].name == 'Admin' or req.user.groups.all()[0].name == 'Broker':
            userForm = UserForm()
        # new lenders (no lender id yet) will get name prepopulated in form
        elif req.user.groups.all()[0].name == 'Lender':
            try:
                # existing lenders are redirected to edit form
                lender_id = req.user.lender.id
                return redirect('loans:edit_lender_form', pk=req.user.lender.id)
            except AttributeError:
                user = { 'first_name': req.user.first_name, \
                         'last_name': req.user.last_name, \
                         'email': req.user.email }
                userForm = UserForm(user)

        lenderForm                 = LenderForm()
        lenderBrokerRelationForm   = LenderBrokerRelationForm()
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
        'lenderBrokerRelationForm': lenderBrokerRelationForm,
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

    return HttpResponse(tmpl.render(context, req))
# END def lender_form



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Client').count() == 0, login_url='/denied/')
def edit_lender_form(req, pk):
    tmpl           = loader.get_template('lender/form.html')
    qualifiers     = Qualifier.objects.order_by('name')
    property_types = PropertyType.objects.order_by('name')
    submit         = 'Update'

    lender = get_object_or_404(Lender, id=pk)
    user   = get_object_or_404(User, id=lender.user.id)

    # TODO refactor (create function that returns dictionary of objects)
    try:
        brkr_rel = LenderBrokerRelation.objects.get(lender=pk)
    except LenderBrokerRelation.DoesNotExist:
        brkr_rel = None

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
        lenderBrokerRelationForm   = LenderBrokerRelationForm(req.POST, instance=brkr_rel)
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
           lenderBrokerRelationForm.is_valid() and \
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


            # TODO shorten
            brk_rel = lenderBrokerRelationForm.save(commit=False)
            brk_rel.lender = lender
            brk_rel.save()

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

            lender.qualifiers.clear()
            for q in req.POST.getlist('qualifier'):
                lender.qualifiers.add(q)

            lender.propertytypes.clear()
            for p in req.POST.getlist('property_type'):
                lender.propertytypes.add(p)

            lenderForm.save_m2m()

            return redirect('loans:lender_detail', pk=lender.id)

    # XXX BEWARE if form is invalid, it will break
    else:
        userForm                   = UserForm(instance=user)
        lenderForm                 = LenderForm(instance=lender)
        lenderBrokerRelationForm   = LenderBrokerRelationForm(instance=brkr_rel)
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
        'lenderBrokerRelationForm': lenderBrokerRelationForm,
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
@user_passes_test(lambda u: u.groups.filter(name='Client').count() == 0, login_url='/denied/')
def lender_list(req):
    templ = loader.get_template('lender/list.html')

    lender_list = Lender.objects.all().select_related('user')
    context = {
        'lenders': lender_list,
    }

    return HttpResponse(templ.render(context, req))
# END lender_list


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Client').count() == 0, login_url='/denied/')
def lender_detail(req, pk):
    templ = loader.get_template('lender/detail.html')
    lender = get_object_or_404(Lender.objects.select_related('user', 'lendertype'), id=pk)

    # TODO shorten
    # https://stackoverflow.com/questions/4353147/whats-the-best-way-to-handle-djangos-objects-get
    try:
        brkr_rel = LenderBrokerRelation.objects.get(lender=pk)
    except LenderBrokerRelation.DoesNotExist:
        brkr_rel = None

    try:
        oo = LenderOwnerOccupiedRE.objects.get(lender=pk)
    except LenderOwnerOccupiedRE.DoesNotExist:
        oo = None

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
        'broker_rel': brkr_rel,
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
# END lender_detail


################################################################################
# BROKER VIEWS
################################################################################

@login_required
#@user_passes_test(lambda u: u.groups.filter(name='client').count() == 0, login_url='/denied/')
def broker_form(req):
    tmpl = loader.get_template('broker/form.html')
    submit = 'Submit'

    if req.method == 'POST':
        # save user info if the req.user is a broker
        if req.user.groups.all()[0].name == 'Broker':
            userForm = UserForm(req.POST, instance=req.user)
        # XXX consider using elif admin, else deny
        # create new user if req.user is admin
        else:
            default_password = 'changeM3!'
            # default user name is first initial, last name
            default_username = (req.POST['first_name'][0] + req.POST['last_name']).lower()
            group = Group.objects.get(name='Broker')

            # TODO check if username exists, if exists, append 01
            new_user = User.objects.create_user(default_username, req.POST['email'], default_password)
            new_user.groups.add(group)
            new_user.save()
            userForm = UserForm(req.POST, instance=new_user)
            brokerForm = BrokerForm(req.POST)

        brokerForm = BrokerForm(req.POST)

        if userForm.is_valid() and \
           brokerForm.is_valid():
            user = userForm.save()

            broker = brokerForm.save(commit=False)
            broker.user = user
            broker.save()

            return redirect('loans:brokers')

    # XXX BEWARE if form is invalid, it will break
    else:
        ## Only Admin can create new brokers
        if req.user.groups.all()[0].name == 'Admin':
            userForm = UserForm()
            brokerForm = BrokerForm()
        # new lenders (no lender id yet) will get name prepopulated in form
        elif req.user.groups.all()[0].name == 'Broker':
            try:
                # existing brokers are redirected to edit form
                broker_id = req.user.broker.id
                return redirect('loans:edit_broker_form', pk=req.user.broker.id)
            except AttributeError:
                user = { 'first_name': req.user.first_name,
                         'last_name': req.user.last_name,
                         'email': req.user.email }
                userForm = UserForm(user)
                brokerForm = BrokerForm(user)

    context = {
        'userForm': userForm,
        'brokerForm': brokerForm,
        'submit': submit,
    }

    return HttpResponse(tmpl.render(context, req))
# END def broker_form



@login_required
#@user_passes_test(lambda u: u.groups.filter(name='Client').count() == 0, login_url='/denied/')
def edit_broker_form(req, pk):
    tmpl   = loader.get_template('broker/form.html')
    submit = 'Update'

    broker = get_object_or_404(Broker, id=pk)
    user   = get_object_or_404(User, id=broker.user.id)


    if req.method == 'POST':
        userForm   = UserForm(req.POST, instance=user)
        brokerForm = BrokerForm(req.POST, instance=broker)

        # TODO refactor: create function to check all necessary forms
        if userForm.is_valid() and \
           brokerForm.is_valid():

            user = userForm.save()

            broker = brokerForm.save(commit=False)
            broker.user = user
            broker.save()

            return redirect('loans:broker_detail', pk=broker.id)

    # XXX BEWARE if form is invalid, it will break
    else:
        userForm   = UserForm(instance=user)
        brokerForm = BrokerForm(instance=broker)


    context = {
        'broker': broker,
        'userForm': userForm,
        'brokerForm': brokerForm,
        'submit': submit,
    }

    return HttpResponse(tmpl.render(context, req))
# END def edit_broker_form


@login_required
#@user_passes_test(lambda u: u.groups.filter(name='client').count() == 0, login_url='/denied/')
def broker_list(req):
    templ = loader.get_template('broker/list.html')

    broker_list = Broker.objects.all().select_related('user')
    context = {
        'brokers': broker_list,
    }

    return HttpResponse(templ.render(context, req))
# END broker_list


@login_required
#@user_passes_test(lambda u: u.groups.filter(name='Client').count() == 0, login_url='/denied/')
def broker_detail(req, pk):
    templ = loader.get_template('broker/detail.html')
    broker = get_object_or_404(Broker.objects.select_related('user'), id=pk)

    context = {
        'broker_data': broker,
    }

    return HttpResponse(templ.render(context, req))
# END lender_detail


################################################################################
# CLIENT VIEWS
################################################################################

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Lender').count() == 0, login_url='/denied/')
def client_form(req):
    tmpl   = loader.get_template('client/form.html')
    submit = 'Submit'
    if req.method == 'POST':
        if req.user.groups.all()[0].name == 'Client':
            userForm = UserForm(req.POST, instance=req.user)
        else:
            default_password = 'changeM3!'
            # default user name is first initial, last name
            default_username = (req.POST['first_name'][0] + req.POST['last_name']).lower()
            group = Group.objects.get(name='Lender')

            new_user = User.objects.create_user(default_username, req.POST['email'], default_password)
            new_user.groups.add(group)
            new_user.save()
            userForm = UserForm(req.POST, instance=new_user)

        clientForm = ClientForm(req.POST)

        if userForm.is_valid() and \
           clientForm.is_valid():

            user = userForm.save()
            client = clientForm.save(commit=False)
            client.user = user

            # if req.user is a Broker, set new lender to broker
            try:
                client.broker = req.user.broker
            except ObjectDoesNotExist:
                client.broker = None

            client.save()

            return redirect('loans:clients')

    else:
        if req.user.groups.all()[0].name == 'Admin' or req.user.groups.all()[0].name == 'Broker':
            userForm = UserForm()
        elif req.user.groups.all()[0].name == 'Client':
            try:
                client_id = req.user.client.id
                return redirect('loans:edit_client_form', pk=req.user.client.id)
            except AttributeError:
                user = {
                    'first_name': req.user.first_name,
                    'last_name': req.user.last_name,
                    'email': req.user.email,
                }
                userForm = UserForm(user)

        clientForm = ClientForm()

    context = {
        'userForm': userForm,
        'clientForm': clientForm,
        'submit': submit,
    }
    return HttpResponse(tmpl.render(context, req))

# END client_form


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Lender').count() == 0, login_url='/denied/')
def edit_client_form(req, pk):
    tmpl   = loader.get_template('client/form.html')
    submit = 'Update'

    client = get_object_or_404(Client, id=pk)
    user   = get_object_or_404(User, id=client.user.id)

    if req.method == 'POST':
        userForm   = UserForm(req.POST, instance=user)
        clientForm = ClientForm(req.POST, instance=client)

        # TODO refactor: create function to check all necessary forms
        if userForm.is_valid() and \
           clientForm.is_valid():

            user = userForm.save()

            client = clientForm.save(commit=False)
            client.user = user
            client.save()

            return redirect('loans:client_detail', pk=client.id)

    # XXX BEWARE if form is invalid, it will break
    else:
        userForm   = UserForm(instance=user)
        clientForm = ClientForm(instance=client)


    context = {
        'client': client,
        'userForm': userForm,
        'clientForm': clientForm,
        'submit': submit,
    }

    return HttpResponse(tmpl.render(context, req))
# END def edit_client_form


@login_required
@user_passes_test(lambda u: u.groups.filter(name='lender').count() == 0, login_url='/denied/')
def client_list(req):
    template = loader.get_template('client/list.html')
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }

    return HttpResponse(template.render(context, req))
# END client_list


@login_required
#@user_passes_test(lambda u: u.groups.filter(name='client').count() == 0, login_url='/denied/')
def client_detail(req, pk):
    templ = loader.get_template('client/detail.html')
    broker = get_object_or_404(Broker.objects.select_related('user'), id=pk)

    context = {
        'broker_data': broker,
    }

    return HttpResponse(templ.render(context, req))
# END client_detail
