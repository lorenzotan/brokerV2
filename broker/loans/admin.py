from django.contrib import admin
from .models import Broker, Lender, Client, Qualifier, PropertyType
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
    writer.writerow([
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
        smart_str(u"Client Using POC"),

        smart_str(u"POC Name"),
        smart_str(u"POC Company"),
        smart_str(u"POC Work Phone"),
        smart_str(u"POC Cell Phone"),
        smart_str(u"POC Email"),

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

        smart_str(u"Business Name"),
        smart_str(u"Business Main Phone"),
        smart_str(u"Business Website"),
        smart_str(u"Business Type"),
        smart_str(u"Year Business Established"),
    ])

    for obj in queryset:
        writer.writerow([
            smart_str(obj.client_first_name),
            smart_str(obj.client_last_name),
            smart_str(obj.client_street_address),
            smart_str(obj.client_city),
            smart_str(obj.client_state),
            smart_str(obj.client_zip_code),
            smart_str(obj.client_work_email),
            smart_str(obj.client_personal_email),
            smart_str(obj.client_work_phone),
            smart_str(obj.client_cell_phone),
            smart_str(obj.client_using_poc),

            smart_str(obj.POC_name),
            smart_str(obj.POC_business),
            smart_str(obj.POC_work_phone),
            smart_str(obj.POC_cell_phone),
            smart_str(obj.POC_email),

            smart_str(obj.client_occupation),
            smart_str(obj.client_company_name),
            smart_str(obj.client_company_street_address),
            smart_str(obj.client_company_city),
            smart_str(obj.client_company_state),
            smart_str(obj.client_company_zip),

            smart_str(obj.loan_amount),
            smart_str(obj.loan_to_value),
            smart_str(obj.loan_dcsr),
            smart_str(obj.loan_desc),

            smart_str(obj.fin_salary),
            smart_str(obj.fin_years_in_business),
            smart_str(obj.fin_total_debt),
            smart_str(obj.fin_monthly_payments),
            smart_str(obj.fin_fico),
            smart_str(obj.fin_owns_home),
            smart_str(obj.fin_bankruptcy),
            smart_str(obj.fin_short_sale),

            smart_str(obj.property_address),
            smart_str(obj.property_value),

            smart_str(obj.docs_executive_summary),
            smart_str(obj.docs_credit_report),
            smart_str(obj.docs_personal_taxes),
            smart_str(obj.docs_business_taxes),
            smart_str(obj.docs_P_and_L),
            smart_str(obj.docs_expense_report),
            smart_str(obj.docs_brokers_opinion),
            smart_str(obj.docs_appraisal),
            smart_str(obj.docs_environmental),
            smart_str(obj.docs_rent_roll),
            smart_str(obj.docs_lease_agreements),

            smart_str(obj.business_name),
            smart_str(obj.business_main_phone),
            smart_str(obj.business_website),
            smart_str(obj.business_type),
            smart_str(obj.business_year_established),



        ])
    return response
export_client_csv.short_description = u"Client Export CSV"

class ClientAdmin(admin.ModelAdmin):
    actions = [export_client_csv]

# NOTE disable till fields are fixed
#admin.site.register(Client, ClientAdmin)


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
        smart_str(u"Owner Occ. Other?"),

        smart_str(u"Investment Office?"),
        smart_str(u"Investment Warehouse?"),
        smart_str(u"Investment Manufacturing?"),
        smart_str(u"Investment Medical?"),
        smart_str(u"Investment Mixed Use?"),
        smart_str(u"Investment Other?"),

        smart_str(u"MultiFamily 2 to 4"),
        smart_str(u"MultiFamily more than 4"),

        smart_str(u"Construction Renovation"),
        smart_str(u"Construction Ground Up Spec"),
        smart_str(u"Construction Commercial"),
        smart_str(u"Construction Residential"),
        smart_str(u"Construction Investment with Land"),
        smart_str(u"Construction Owner Occ with Land"),

        smart_str(u"SBA 7a?"),
        smart_str(u"SBA 504?"),
        smart_str(u"SBA CAPline?"),
        smart_str(u"SBA Microloan?"),
        smart_str(u"SBA Other?"),

        smart_str(u"HELOC 1st Position"),
        smart_str(u"HELOC 2nd Position"),

        smart_str(u"BLOC Residential Property"),
        smart_str(u"BLOC Stocks"),
        smart_str(u"BLOC Savings"),
        smart_str(u"BLOC Investment Property"),
        smart_str(u"BLOC 1st Position"),
        smart_str(u"BLOC 2nd Position"),

        smart_str(u"Bridge?"),
    ]

    for q in q_obj:
        qualifiers[q.id] = q.name

    for q_id in sorted(qualifiers):
        header.append(smart_str(qualifiers[q_id]))

    for p in pt_obj:
        propertytypes[p.id] = p.name

    for pt_id in sorted(propertytypes):
        header.append(smart_str(propertytypes[pt_id]))

    writer.writerow(
        header
    )

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
        # XXX didn't have to do else before
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
                smart_str(bools[lender.lenderowneroccupiedre.other]),
            ])

        if hasattr(lender, 'lenderinvestmentre'):
            fields.extend([
                smart_str(bools[lender.lenderinvestmentre.office]),
                smart_str(bools[lender.lenderinvestmentre.warehouse]),
                smart_str(bools[lender.lenderinvestmentre.manufacturing]),
                smart_str(bools[lender.lenderinvestmentre.medical]),
                smart_str(bools[lender.lenderinvestmentre.mixed_use]),
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
            ])

        if hasattr(lender, 'lendersbaloan'):
            fields.extend([
                smart_str(bools[lender.lendersbaloan.sba_7a]),
                smart_str(bools[lender.lendersbaloan.sba_504]),
                smart_str(bools[lender.lendersbaloan.CAPline]),
                smart_str(bools[lender.lendersbaloan.micro]),
                smart_str(bools[lender.lendersbaloan.other]),
            ])

        if hasattr(lender, 'lenderhelocloan'):
            fields.extend([
                smart_str(bools[lender.lenderhelocloan.pos_1]),
                smart_str(bools[lender.lenderhelocloan.pos_2]),
            ])

        if hasattr(lender, 'lenderblocloan'):
            fields.extend([
                smart_str(bools[lender.lenderblocloan.resid_prop]),
                smart_str(bools[lender.lenderblocloan.stocks]),
                smart_str(bools[lender.lenderblocloan.savings]),
                smart_str(bools[lender.lenderblocloan.inv_prop]),
                smart_str(bools[lender.lenderblocloan.pos1]),
                smart_str(bools[lender.lenderblocloan.pos2]),
            ])

        if hasattr(lender, 'lenderbridgeloan'):
            fields.extend([
                smart_str(bools[lender.lenderbridgeloan.bridge]),
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
