from django.contrib import admin
from .models import Lender, Client
from django.http import HttpResponse

# http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
# ... export functions will go here ...
def export_client_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Client First Name"),
        smart_str(u"Client Last Name"),
        smart_str(u"Client Street Address"),
        smart_str(u"Client City"),
        smart_str(u"Client State"),
        smart_str(u"Client Zip Code"),
        smart_str(u"Client Work Email"),
        smart_str(u"Client Personal Email"),
        smart_str(u"Client Work Phone"),
        smart_str(u"Client Cell Phone"),
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
export_client_csv.short_description = u"Export Client CSV"

class ClientAdmin(admin.ModelAdmin):
    actions = [export_client_csv]

# NOTE disable till fields are fixed
#admin.site.register(Client, ClientAdmin)

def export_lender_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Lender First Name"),
        smart_str(u"Lender Last Name"),
        smart_str(u"Lender Company"),
        smart_str(u"Lender Street Address"),
        smart_str(u"Lender City"),
        smart_str(u"Lender State"),
        smart_str(u"Lender Zip Code"),
        smart_str(u"Lender Work Email"),
        smart_str(u"Lender Personal Email"),
        smart_str(u"Lender Work Phone"),
        smart_str(u"Lender Cell Phone"),
        smart_str(u"Lender Solicitation?"),

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

        smart_str(u"HELOC?"),
        smart_str(u"BLOC?"),
        smart_str(u"Bridge?"),

        smart_str(u"Pays Brokers fees?"),
        smart_str(u"Outside CA?"),
        smart_str(u"1031 Exchange"),
        smart_str(u"Less than 500K"),
        smart_str(u"Less than 1M"),
        smart_str(u"Equipment Purchase"),
        smart_str(u"Nonconforming Property"),
        smart_str(u"Ground Lease"),
        smart_str(u"Cannabis"),
        smart_str(u"Interest Only"),
        smart_str(u"Revocable Trust"),
        smart_str(u"Irrevocable Trust"),
        smart_str(u"Foreclosure"),
        smart_str(u"Single Tenant"),
        smart_str(u"Bankruptcy"),
        smart_str(u"Entitlements"),
        smart_str(u"Nonprofit"),
        smart_str(u"Cash out Refi"),
        smart_str(u"Non recourse"),
        smart_str(u"Real Estate Collateral"),
        smart_str(u"Cross Collateral"),
        smart_str(u"Business Acquisitions"),

        smart_str(u"Automotive"),
        smart_str(u"Carwash"),
        smart_str(u"Entertainment"),
        smart_str(u"Farm / Agr,"),
        smart_str(u"Gas Station"),
        smart_str(u"Hospital"),
        smart_str(u"Hotel (Flag)"),
        smart_str(u"Hotel (Non-flag)"),
        smart_str(u"Industrial"),
        smart_str(u"Marina"),
        smart_str(u"Medical"),
        smart_str(u"Mobile Home"),
        smart_str(u"Motel (Flag)"),
        smart_str(u"Motel (Non-flag)"),
        smart_str(u"Office"),
        smart_str(u"Restaurant"),
        smart_str(u"Retail"),
        smart_str(u"Senior Housing"),
        smart_str(u"Storage"),
        smart_str(u"Student Housing"),

    ])

    # TODO catch exceptions for tables that do not have related data to lender
    bools = {
        True: 'Yes',
        False: 'No'
    }

    recs = queryset.select_related(
    'lenderowneroccupiedre',
    'lenderinvestmentre',
    'lendermultifamilyloan',
    'lenderconstructionloan',
    'lendersbaloan',
    'lenderhelocloan',
    'lenderblocloan',
    'lenderbridgeloan')

# https://stackoverflow.com/questions/37652520/django-select-related-in-reverse/37792783
    for rec in recs:
        fields = [
            smart_str(rec.user.first_name),
            smart_str(rec.user.last_name),
            smart_str(rec.company),
            smart_str(rec.user.address),
            smart_str(rec.user.city),
            smart_str(rec.user.state),
            smart_str(rec.user.zip_code),
            smart_str(rec.user.email),
            '',
            smart_str(rec.user.phone),
            '',
            smart_str(rec.solicit),
        ]

        # https://stackoverflow.com/questions/10487278/how-to-declare-and-add-items-to-an-array-in-python
        #https://stackoverflow.com/questions/27064206/django-check-if-a-related-object-exists-error-relatedobjectdoesnotexist
        if hasattr(rec, 'lenderowneroccupiedre'):
            fields.extend([
                smart_str(bools[rec.lenderowneroccupiedre.office]),
                smart_str(bools[rec.lenderowneroccupiedre.warehouse]),
                smart_str(bools[rec.lenderowneroccupiedre.manufacturing]),
                smart_str(bools[rec.lenderowneroccupiedre.medical]),
                smart_str(bools[rec.lenderowneroccupiedre.mixed_use]),
                smart_str(bools[rec.lenderowneroccupiedre.other]),
            ])

        if hasattr(rec, 'lenderinvestmentre'):
            fields.extend([
                smart_str(bools[rec.lenderinvestmentre.office]),
                smart_str(bools[rec.lenderinvestmentre.warehouse]),
                smart_str(bools[rec.lenderinvestmentre.manufacturing]),
                smart_str(bools[rec.lenderinvestmentre.medical]),
                smart_str(bools[rec.lenderinvestmentre.mixed_use]),
                smart_str(bools[rec.lenderinvestmentre.other]),
            ])

        if hasattr(rec, 'lendermultifamilyloan'):
            fields.extend([
                smart_str(bools[rec.lendermultifamilyloan.mf_2to4]),
                smart_str(bools[rec.lendermultifamilyloan.mf_gt4]),
            ])

        if hasattr(rec, 'lenderconstructionloan'):
            fields.extend([
                smart_str(bools[rec.lenderconstructionloan.renovation]),
                smart_str(bools[rec.lenderconstructionloan.ground_up_spec]),
                smart_str(bools[rec.lenderconstructionloan.commercial]),
                smart_str(bools[rec.lenderconstructionloan.residential]),
                smart_str(bools[rec.lenderconstructionloan.inv_w_land]),
                smart_str(bools[rec.lenderconstructionloan.oo_w_land]),
            ])

        if hasattr(rec, 'lendersbaloan'):
            fields.extend([
                smart_str(bools[rec.lendersbaloan.sba_7a]),
                smart_str(bools[rec.lendersbaloan.sba_504]),
                smart_str(bools[rec.lendersbaloan.CAPline]),
                smart_str(bools[rec.lendersbaloan.micro]),
                smart_str(bools[rec.lendersbaloan.other]),
            ])

        if hasattr(rec, 'lenderhelocloan'):
            fields.extend([
                smart_str(bools[rec.lenderhelocloan.pos_1]),
                smart_str(bools[rec.lenderhelocloan.pos_2]),
                smart_str(bools[rec.lenderblocloan.resid_prop]),
                smart_str(bools[rec.lenderblocloan.stocks]),
                smart_str(bools[rec.lenderblocloan.savings]),
                smart_str(bools[rec.lenderblocloan.inv_prop]),
                smart_str(bools[rec.lenderblocloan.pos1]),
                smart_str(bools[rec.lenderblocloan.pos2]),
                smart_str(bools[rec.lenderbridgeloan.bridge]),
            ])

# to get qualifiers and property types
# need to map quals with the headers (id to name)
# if lender has id then YES for that field

        writer.writerow(
            fields
            #smart_str(rec.qual_pays_fees),
            #smart_str(rec.qual_outside_ca),
            #smart_str(rec.qual_1031_exchange),
            #smart_str(rec.qual_lt_500K),
            #smart_str(rec.qual_lt_1M),
            #smart_str(rec.qual_equip),
            #smart_str(rec.qual_non_conform),
            #smart_str(rec.qual_ground_lease),
            #smart_str(rec.qual_relationship),
            #smart_str(rec.qual_cannabis),
            #smart_str(rec.qual_io),
            #smart_str(rec.qual_rev_trust),
            #smart_str(rec.qual_irrev_trust),
            #smart_str(rec.qual_foreclosure),
            #smart_str(rec.qual_single_tenant),
            #smart_str(rec.qual_bk),
            #smart_str(rec.qual_entitlements),
            #smart_str(rec.qual_non_profit),
            #smart_str(rec.qual_cashout_refi),
            #smart_str(rec.qual_non_recourse),
            #smart_str(rec.qual_re_collateral),
            #smart_str(rec.qual_cross_collateral),
            #smart_str(rec.qual_biz_acq),

            #smart_str(rec.prop_automotive),
            #smart_str(rec.prop_carwash),
            #smart_str(rec.prop_entertainment),
            #smart_str(rec.prop_farm),
            #smart_str(rec.prop_gas_station),
            #smart_str(rec.prop_hospital),
            #smart_str(rec.prop_hotel_flag),
            #smart_str(rec.prop_hotel_nonflag),
            #smart_str(rec.prop_industrial),
            #smart_str(rec.prop_marina),
            #smart_str(rec.prop_medical),
            #smart_str(rec.prop_mobile_home),
            #smart_str(rec.prop_motel_flag),
            #smart_str(rec.prop_motel_nonflag),
            #smart_str(rec.prop_office),
            #smart_str(rec.prop_restaurant),
            #smart_str(rec.prop_retail),
            #smart_str(rec.prop_senior_housing),
            #smart_str(rec.prop_storage),
            #smart_str(rec.prop_student_housing),
        )
    return response
export_lender_csv.short_description = u"Export Lender CSV"

class LenderAdmin(admin.ModelAdmin):
    actions = [export_lender_csv]

# NOTE disabling until fields are fixed
admin.site.register(Lender, LenderAdmin)
