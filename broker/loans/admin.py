from django.contrib import admin
from .models import Broker, Lender, Client, Qualifier, PropertyType, NeedsList
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.utils.encoding import smart_str
import csv
import datetime

bools = {
    True: 'Yes',
    False: 'No'
}

# https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
# http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
# ... export functions will go here ..


################################################################################
# CLIENT EXPORT
################################################################################
def export_client_csv(modeladmin, request, queryset):
    date = datetime.datetime.now().date()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=client_export_' + str(date) + '.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)

    qualifiers = {}
    needs = {}
    q_obj = Qualifier.objects.all()
    n_obj = NeedsList.objects.all()

    header = [
        smart_str(u"Client First Name"),
        smart_str(u"Client Last Name"),
        smart_str(u"Client Street Address"),
        smart_str(u"Client City"),
        smart_str(u"Client State"),
        smart_str(u"Client Zip Code"),
        smart_str(u"Client Primary Email"),
        smart_str(u"Client Secondary Email"),
        smart_str(u"Client Work Phone"),
        smart_str(u"Client Cell Phone"),
        smart_str(u"Client Fax Phone"),
        smart_str(u"Client Other Phone"),

        #smart_str(u"POC Name"),
        #smart_str(u"POC Company"),
        #smart_str(u"POC Work Phone"),
        #smart_str(u"POC Cell Phone"),
        #smart_str(u"POC Email"),

        smart_str(u"Occupation"),
        smart_str(u"Company Name"),
        smart_str(u"Company Street Address"),
        smart_str(u"Company City"),
        smart_str(u"Company State"),
        smart_str(u"Company Zip"),

        smart_str(u"Loan Amount"),
        smart_str(u"Loan To Value"),
        smart_str(u"Loan DSCR"),
        smart_str(u"Loan Description"),

        smart_str(u"Salary"),
        smart_str(u"Years In Business"),
        smart_str(u"Debt"),
        smart_str(u"Monthly Payments"),
        smart_str(u"FICO"),
        smart_str(u"Owns Home"),
        smart_str(u"Bankruptcy"),
        smart_str(u"Short Sale"),

        smart_str(u"Property Address"),
        smart_str(u"Property Value"),

        smart_str(u"Business Name"),
        smart_str(u"Business Main Phone"),
        smart_str(u"Business Website"),
        smart_str(u"Business Type"),
        smart_str(u"Year Business Established"),
    ]

    for q in q_obj:
        qualifiers[q.id] = q.name

    for q_id in sorted(qualifiers):
        header.append(smart_str(qualifiers[q_id]))


    for n in n_obj:
        needs[n.id] = n.name

    for n_id in sorted(needs):
        header.append(smart_str(needs[n_id]))

    writer.writerow(header)

    client411 = queryset.select_related(
        'clientemploymentinfo',
        'clientloaninfo',
        'clientfinancialinfo',
        'clientpropertyinfo',
        'clientbusinessinfo'
    )

    for client in client411:
        fields = [
            smart_str(client.user.first_name),
            smart_str(client.user.last_name),
            smart_str(client.user.address),
            smart_str(client.user.city),
            smart_str(client.user.state),
            smart_str(client.user.zip_code),
            smart_str(client.user.email),
            smart_str(client.user.email_x),
            smart_str(client.user.phone_w),
            smart_str(client.user.phone_m),
            smart_str(client.user.phone_f),
            smart_str(client.user.phone_o),
        ]

            #smart_str(obj.POC_name),
            #smart_str(obj.POC_business),
            #smart_str(obj.POC_work_phone),
            #smart_str(obj.POC_cell_phone),
            #smart_str(obj.POC_email),

        if hasattr(client, 'clientemploymentinfo'):
            fields.extend([
                smart_str(client.clientemploymentinfo.occupation),
                smart_str(client.clientemploymentinfo.company_name),
                smart_str(client.clientemploymentinfo.address),
                smart_str(client.clientemploymentinfo.city),
                smart_str(client.clientemploymentinfo.state),
                smart_str(client.clientemploymentinfo.zip_code),
            ])
        else:
            fields.extend([
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
            ])

        if hasattr(client, 'clientloaninfo'):
            fields.extend([
                smart_str(client.clientloaninfo.amount),
                smart_str(client.clientloaninfo.loan2val),
                smart_str(client.clientloaninfo.dscr),
                smart_str(client.clientloaninfo.desc),
            ])
        else:
            fields.extend([
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
            ])

        if hasattr(client, 'clientfinancialinfo'):
            fields.extend([
                smart_str(client.clientfinancialinfo.salary),
                smart_str(client.clientfinancialinfo.yrs_in_biz),
                smart_str(client.clientfinancialinfo.debt),
                smart_str(client.clientfinancialinfo.mnthly_pymnts),
                smart_str(client.clientfinancialinfo.fico),
                smart_str(client.clientfinancialinfo.owns_home),
                smart_str(client.clientfinancialinfo.bankruptcy),
                smart_str(client.clientfinancialinfo.short_sale),
            ])
        else:
            fields.extend([
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str('No'),
                smart_str('No'),
            ])

        if hasattr(client, 'clientpropertyinfo'):
            fields.extend([
                smart_str(client.clientpropertyinfo.address),
                smart_str(client.clientpropertyinfo.value),
            ])
        else:
            fields.extend([
                smart_str(''),
                smart_str(''),
            ])

        if hasattr(client, 'clientbusinessinfo'):
            fields.extend([
                smart_str(client.clientbusinessinfo.name),
                smart_str(client.clientbusinessinfo.phone),
                smart_str(client.clientbusinessinfo.url),
                smart_str(client.clientbusinessinfo.btype),
                smart_str(client.clientbusinessinfo.est),
            ])
        else:
            fields.extend([
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
                smart_str(''),
            ])

        client_qualifiers = []

        for q in client.qualifiers.through.objects.filter(client_id = client.id):
            client_qualifiers.append(q.qualifier_id)

        for q_id in sorted(qualifiers):
            if q_id in client_qualifiers:
                fields.append('Yes')
            else:
                fields.append('No')

        client_needs = []

        for n in client.needs.through.objects.filter(client_id = client.id):
            client_needs.append(n.id)

        for n_id in sorted(needs):
            if n_id in client_needs:
                fields.append('Yes')
            else:
                fields.append('No')

        writer.writerow(fields)
    # end for

    return response
export_client_csv.short_description = u"Client Export CSV"

class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ['get_first_name', 'get_last_name']
    actions = [export_client_csv]

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__first_name'

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__last_name'

# end ClientAdmin

# NOTE disable till fields are fixed
admin.site.register(Client, ClientAdmin)


################################################################################
# LENDER EXPORT
################################################################################
def export_lender_csv(modeladmin, request, queryset):

    date = datetime.datetime.now().date()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=lender_export_' + str(date) + '.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)

    qualifiers = {}
    propertytypes = {}

    q_obj = Qualifier.objects.all()
    pt_obj = PropertyType.objects.all()

    header = [
        smart_str(u"Lender First Name"),
        smart_str(u"Lender Last Name"),
        smart_str(u"Lender Company"),
        smart_str(u"Lender Street Address"),
        smart_str(u"Lender City"),
        smart_str(u"Lender State"),
        smart_str(u"Lender Zip Code"),
        smart_str(u"Lender Primary Email"),
        smart_str(u"Lender Secondary Email"),
        smart_str(u"Lender Work Phone"),
        smart_str(u"Lender Mobile Phone"),
        smart_str(u"Lender Fax Phone"),
        smart_str(u"Lender Other Phone"),
        smart_str(u"Lender Type"),
        smart_str(u"Loan Amount"),

        smart_str(u"Lender Solicitation?"),
        smart_str(u"Pays Broker Fees?"),
        smart_str(u"Pays Broker Rebate?"),
        smart_str(u"Pays via 1099?"),
        smart_str(u"Pays through Escrow?"),

        smart_str(u"Owner Occ. Office?"),
        smart_str(u"Owner Occ. Warehouse?"),
        smart_str(u"Owner Occ. Manufacturing?"),
        smart_str(u"Owner Occ. Medical?"),
        smart_str(u"Owner Occ. Mixed Use?"),
        smart_str(u"Owner Occ. Industrial?"),
        smart_str(u"Owner Occ. Other?"),

        smart_str(u"Investment Office?"),
        smart_str(u"Investment Warehouse?"),
        smart_str(u"Investment Manufacturing?"),
        smart_str(u"Investment Medical?"),
        smart_str(u"Investment Mixed Use?"),
        smart_str(u"Investment Industrial?"),
        smart_str(u"Investment Other?"),

        smart_str(u"MultiFamily 2 to 4"),
        smart_str(u"MultiFamily more than 4"),

        smart_str(u"Construction Renovation"),
        smart_str(u"Construction Ground Up Spec"),
        smart_str(u"Construction Commercial"),
        smart_str(u"Construction Residential"),
        smart_str(u"Construction Investment with Land"),
        smart_str(u"Construction Owner Occ with Land"),
        smart_str(u"Construction Investor"),

        smart_str(u"SBA 7a?"),
        smart_str(u"SBA 504?"),
        smart_str(u"SBA CAPline?"),
        smart_str(u"SBA Microloan?"),
        smart_str(u"SBA Express?"),
        smart_str(u"SBA ITL?"),
        smart_str(u"SBA Other?"),

        smart_str(u"HELOC 1st Position"),
        smart_str(u"HELOC 2nd Position"),
        smart_str(u"HELOC 3rd Position"),

        smart_str(u"BLOC Residential Property"),
        smart_str(u"BLOC Stocks"),
        smart_str(u"BLOC Savings"),
        smart_str(u"BLOC Investment Property"),
        smart_str(u"BLOC 1st Position"),
        smart_str(u"BLOC 2nd Position"),
        smart_str(u"BLOC Equipment"),
        smart_str(u"BLOC Working Capital"),
        smart_str(u"BLOC Interest Only"),
        smart_str(u"BLOC Secured by Accts Receivable"),
        smart_str(u"BLOC Secured by Inventory"),
        smart_str(u"BLOC RE Secured"),
        smart_str(u"BLOC RE Unsecured"),

        smart_str(u"Bridge?"),
        smart_str(u"Commercial Term?"),
        smart_str(u"USDA?"),
        smart_str(u"Stated Income?"),
    ]

    for q in q_obj:
        qualifiers[q.id] = q.name

    for q_id in sorted(qualifiers):
        header.append(smart_str(qualifiers[q_id]))

    for p in pt_obj:
        propertytypes[p.id] = p.name

    for pt_id in sorted(propertytypes):
        header.append(smart_str(propertytypes[pt_id]))

    writer.writerow(header)

    lender411 = queryset.select_related(
                'lenderbrokerrelation',
                'lenderowneroccupiedre',
                'lenderinvestmentre',
                'lendermultifamilyloan',
                'lenderconstructionloan',
                'lendersbaloan',
                'lenderhelocloan',
                'lenderblocloan',
                'lenderbridgeloan')

# https://stackoverflow.com/questions/37652520/django-select-related-in-reverse/37792783
    for lender in lender411:
        fields = [
            smart_str(lender.user.first_name),
            smart_str(lender.user.last_name),
            smart_str(lender.company),
            smart_str(lender.user.address),
            smart_str(lender.user.city),
            smart_str(lender.user.state),
            smart_str(lender.user.zip_code),
            smart_str(lender.user.email),
            smart_str(lender.user.email_x),
            smart_str(lender.user.phone_w),
            smart_str(lender.user.phone_m),
            smart_str(lender.user.phone_f),
            smart_str(lender.user.phone_o),
            smart_str(lender.lendertype),
            smart_str(lender.loanamt),
        ]

        # https://stackoverflow.com/questions/10487278/how-to-declare-and-add-items-to-an-array-in-python
        # https://stackoverflow.com/questions/27064206/django-check-if-a-related-object-exists-error-relatedobjectdoesnotexist
        if hasattr(lender, 'lenderbrokerrelation'):
            fields.extend([
                smart_str(lender.lenderbrokerrelation.solicit),
                smart_str(bools[lender.lenderbrokerrelation.pays_brkr_fees]),
                smart_str(bools[lender.lenderbrokerrelation.pays_brkr_rebate]),
                smart_str(bools[lender.lenderbrokerrelation.pays_1099]),
                smart_str(bools[lender.lenderbrokerrelation.pays_escrow]),
            ])
        else:
            fields.extend([
                smart_str(''),
                smart_str('No'),
                smart_str('No'),
                smart_str('No'),
                smart_str('No'),
            ])

        if hasattr(lender, 'lenderowneroccupiedre'):
            fields.extend([
                smart_str(bools[lender.lenderowneroccupiedre.office]),
                smart_str(bools[lender.lenderowneroccupiedre.warehouse]),
                smart_str(bools[lender.lenderowneroccupiedre.manufacturing]),
                smart_str(bools[lender.lenderowneroccupiedre.medical]),
                smart_str(bools[lender.lenderowneroccupiedre.mixed_use]),
                smart_str(bools[lender.lenderowneroccupiedre.industrial]),
                smart_str(bools[lender.lenderowneroccupiedre.other]),
            ])

        if hasattr(lender, 'lenderinvestmentre'):
            fields.extend([
                smart_str(bools[lender.lenderinvestmentre.office]),
                smart_str(bools[lender.lenderinvestmentre.warehouse]),
                smart_str(bools[lender.lenderinvestmentre.manufacturing]),
                smart_str(bools[lender.lenderinvestmentre.medical]),
                smart_str(bools[lender.lenderinvestmentre.mixed_use]),
                smart_str(bools[lender.lenderinvestmentre.industrial]),
                smart_str(bools[lender.lenderinvestmentre.other]),
            ])

        if hasattr(lender, 'lendermultifamilyloan'):
            fields.extend([
                smart_str(bools[lender.lendermultifamilyloan.mf_2to4]),
                smart_str(bools[lender.lendermultifamilyloan.mf_gt4]),
            ])

        if hasattr(lender, 'lenderconstructionloan'):
            fields.extend([
                smart_str(bools[lender.lenderconstructionloan.renovation]),
                smart_str(bools[lender.lenderconstructionloan.ground_up_spec]),
                smart_str(bools[lender.lenderconstructionloan.commercial]),
                smart_str(bools[lender.lenderconstructionloan.residential]),
                smart_str(bools[lender.lenderconstructionloan.inv_w_land]),
                smart_str(bools[lender.lenderconstructionloan.oo_w_land]),
                smart_str(bools[lender.lenderconstructionloan.investor]),
            ])

        if hasattr(lender, 'lendersbaloan'):
            fields.extend([
                smart_str(bools[lender.lendersbaloan.sba_7a]),
                smart_str(bools[lender.lendersbaloan.sba_504]),
                smart_str(bools[lender.lendersbaloan.CAPline]),
                smart_str(bools[lender.lendersbaloan.micro]),
                smart_str(bools[lender.lendersbaloan.express]),
                smart_str(bools[lender.lendersbaloan.itl]),
                smart_str(bools[lender.lendersbaloan.other]),
            ])

        if hasattr(lender, 'lenderhelocloan'):
            fields.extend([
                smart_str(bools[lender.lenderhelocloan.pos_1]),
                smart_str(bools[lender.lenderhelocloan.pos_2]),
                smart_str(bools[lender.lenderhelocloan.pos_3]),
            ])

        if hasattr(lender, 'lenderblocloan'):
            fields.extend([
                smart_str(bools[lender.lenderblocloan.resid_prop]),
                smart_str(bools[lender.lenderblocloan.stocks]),
                smart_str(bools[lender.lenderblocloan.savings]),
                smart_str(bools[lender.lenderblocloan.inv_prop]),
                smart_str(bools[lender.lenderblocloan.pos1]),
                smart_str(bools[lender.lenderblocloan.pos2]),
                smart_str(bools[lender.lenderblocloan.equipment]),
                smart_str(bools[lender.lenderblocloan.work_cap]),
                smart_str(bools[lender.lenderblocloan.int_only]),
                smart_str(bools[lender.lenderblocloan.sec_accts_rec]),
                smart_str(bools[lender.lenderblocloan.sec_inv]),
                smart_str(bools[lender.lenderblocloan.re_secure]),
                smart_str(bools[lender.lenderblocloan.re_unsecure]),
            ])

        if hasattr(lender, 'lenderbridgeloan'):
            fields.extend([
                smart_str(bools[lender.lenderbridgeloan.bridge]),
                smart_str(bools[lender.lenderbridgeloan.comm_term]),
                smart_str(bools[lender.lenderbridgeloan.usda]),
                smart_str(bools[lender.lenderbridgeloan.stated_inc]),
            ])


        # XXX could use a refactor here
        lender_qualifiers = []

        for q in lender.qualifiers.through.objects.filter(lender_id = lender.id):
            lender_qualifiers.append(q.qualifier_id)

        for q_id in sorted(qualifiers):
            if q_id in lender_qualifiers:
                fields.append('Yes')
            else:
                fields.append('No')


        lender_propertytypes = []

        for pt in lender.propertytypes.through.objects.filter(lender_id = lender.id):
            lender_propertytypes.append(pt.propertytype_id)

        for pt_id in sorted(propertytypes):
            if pt_id in lender_propertytypes:
                fields.append('Yes')
            else:
                fields.append('No')

        writer.writerow(fields)
    # end for

    return response
# end def 

export_lender_csv.short_description = u"Lender CSV Export"

# get_name
# https://stackoverflow.com/questions/163823/can-list-display-in-a-django-modeladmin-display-attributes-of-foreignkey-field
class LenderAdmin(admin.ModelAdmin):
    model = Lender
    list_display = ['get_first_name', 'get_last_name']
    actions = [export_lender_csv]

    #def get_name(self, obj):
    #    return obj.user.first_name + ' ' + obj.user.last_name
    #get_name.admin_order_field = Concat('user__first_name', Value(' '), 'user__last_name')

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__first_name'

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__last_name'

# end LenderAdmin

# NOTE disabling until fields are fixed
admin.site.register(Lender, LenderAdmin)




################################################################################
# BROKER EXPORT
################################################################################
def export_broker_csv(modeladmin, request, queryset):

    date = datetime.datetime.now().date()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=broker_export_' + str(date) + '.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)

    header = [
        smart_str(u"Broker First Name"),
        smart_str(u"Broker Last Name"),
        smart_str(u"Broker Company"),
        smart_str(u"Broker Street Address"),
        smart_str(u"Broker City"),
        smart_str(u"Broker State"),
        smart_str(u"Broker Zip Code"),
        smart_str(u"Broker Primary Email"),
        smart_str(u"Broker Secondary Email"),
        smart_str(u"Broker Work Phone"),
        smart_str(u"Broker Mobile Phone"),
        smart_str(u"Broker Fax Phone"),
        smart_str(u"Broker Other Phone"),
    ]

    writer.writerow(
        header
    )

# https://stackoverflow.com/questions/37652520/django-select-related-in-reverse/37792783
    for broker in queryset:
        fields = [
            smart_str(broker.user.first_name),
            smart_str(broker.user.last_name),
            smart_str(broker.company),
            smart_str(broker.user.address),
            smart_str(broker.user.city),
            smart_str(broker.user.state),
            smart_str(broker.user.zip_code),
            smart_str(broker.user.email),
            smart_str(broker.user.email_x),
            smart_str(broker.user.phone_w),
            smart_str(broker.user.phone_m),
            smart_str(broker.user.phone_f),
            smart_str(broker.user.phone_o),
        ]

        writer.writerow(fields)
    # end for

    return response
# end def export_broker_csv

export_broker_csv.short_description = u"Broker CSV Export"

# get_name
# https://stackoverflow.com/questions/163823/can-list-display-in-a-django-modeladmin-display-attributes-of-foreignkey-field
class BrokerAdmin(admin.ModelAdmin):
    model = Broker
    list_display = ['get_first_name', 'get_last_name']
    actions = [export_broker_csv]

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__first_name'

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__last_name'


admin.site.register(Broker, BrokerAdmin)
