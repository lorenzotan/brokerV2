from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

#NOTE: Meta options: https://docs.djangoproject.com/en/dev/ref/models/options/

# Create your models here.
class Qualifier(models.Model):
    name = models.CharField(max_length=50, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LoanType(models.Model):
    name  = models.CharField(max_length=50, default=None, null=True, blank=True)
    client_model = models.CharField(max_length=50, default=None, null=True, blank=True)
    client_form  = models.CharField(max_length=50, default=None, null=True, blank=True)
    lender_model = models.CharField(max_length=50, default=None, null=True, blank=True)
    lender_form  = models.CharField(max_length=50, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
    

class PropertyType(models.Model):
    name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class NeedsList(models.Model):
    name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LoanPurpose(models.Model):
    name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PointOfContact(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    last_name  = models.CharField(max_length=50, default=None, null=True, blank=True)
    company    = models.CharField(max_length=100, default=None, null=True, blank=True)
    w_email    = models.EmailField(max_length=100, default=None, null=True, blank=True)
    m_phone    = models.CharField(max_length=10, blank=True)
    w_phone    = models.CharField(max_length=10, blank=True)


class ClientBusinessInfo(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation   = models.CharField(max_length=50, default=None, null=True, blank=True)
    company_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    address      = models.CharField(max_length=50, default=None, null=True, blank=True)
    city         = models.CharField(max_length=50, default=None, null=True, blank=True)
    state        = models.CharField(max_length=2, default=None, null=True, blank=True)
    zip_code     = models.CharField(max_length=10, default=None, null=True, blank=True)


class ClientLoanInfo(models.Model):
    # NOTE for currency
    # https://stackoverflow.com/questions/1139393/what-is-the-best-django-model-field-to-use-to-represent-a-us-dollar-amount
    # https://github.com/django-money/django-money
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount   = models.DecimalField(max_digits=17, decimal_places=2)
    loan2val = models.DecimalField(max_digits=17, decimal_places=2)
    dscr     = models.DecimalField(max_digits=17, decimal_places=2)
    desc     = models.TextField()


class ClientFinancialInfo(models.Model):
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salary        = models.DecimalField(max_digits=17, decimal_places=2)
    yrs_in_biz    = models.PositiveSmallIntegerField()
    debt          = models.DecimalField(max_digits=17, decimal_places=2)
    mnthly_pymnts = models.DecimalField(max_digits=17, decimal_places=2)
    fico          = models.PositiveSmallIntegerField()
    owns_home     = models.BooleanField()
    bankruptcy    = models.BooleanField()
    short_sale    = models.BooleanField()


class ClientPropertyInfo(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, default=None, null=True, blank=True)
    value   = models.DecimalField(max_digits=17, decimal_places=2)


class Broker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Client(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    loantype   = models.ForeignKey(LoanType, on_delete=models.SET_NULL, blank=True, null=True)
    poc        = models.ManyToManyField(PointOfContact)
    business   = models.ForeignKey(ClientBusinessInfo, on_delete=models.SET_NULL, blank=True, null=True)
    qualifiers = models.ManyToManyField(Qualifier)
    needslist  = models.ManyToManyField(NeedsList)
    broker     = models.ForeignKey(Broker, on_delete=models.SET_NULL, blank=True, null=True)


class LenderType(models.Model):
    name = models.CharField(max_length=50, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Lender(models.Model):
    user          = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company       = models.CharField(max_length=100, default=None, null=True, blank=True)
    qualifiers    = models.ManyToManyField(Qualifier)
    propertytypes = models.ManyToManyField(PropertyType)
    solicit       = models.PositiveSmallIntegerField()
    broker        = models.ForeignKey(Broker, on_delete=models.SET_NULL, blank=True, null=True)
    lendertype    = models.ForeignKey(LenderType, on_delete=models.SET_NULL, blank=True, null=True)


class ClientBLOCLoan(models.Model):
    client         = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    name           = models.CharField(max_length=50, default='', blank=True, null=True)
    address        = models.CharField(max_length=50, default='', blank=True, null=True)
    annual_receipt = models.CharField(max_length=25, verbose_name="Business Name")
    loan_amt       = models.IntegerField(verbose_name="Loan Amount")
    term           = models.IntegerField(default='', verbose_name="Business Name")


class ClientConstructionLoan(models.Model):
    client        = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    property_type = models.CharField(max_length=50, default='', blank=True, null=True)
    address       = models.CharField(max_length=50, default='', blank=True, null=True)
    architect     = models.CharField(max_length=50, default='', blank=True, null=True)
    contractor    = models.CharField(max_length=50, default='', blank=True, null=True)
    bridge        = models.NullBooleanField(default=None)
    land          = models.NullBooleanField(default=None)


class ClientMixedUseLoan(models.Model):
    client         = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    property_type  = models.CharField(max_length=25, default='', blank=True, null=True)
    business_list  = models.CharField(max_length=50, default='', blank=True, null=True)
    annual_rent    = models.IntegerField(blank=True, null=True)
    annual_expense = models.IntegerField(blank=True, null=True)
    purpose        = models.OneToOneField(LoanPurpose, on_delete=models.CASCADE, null=True)
    cash_out       = models.NullBooleanField(default=None)


class ClientMultiFamilyLoan(models.Model):
    client          = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    number_of_units = models.IntegerField()
    year_built      = models.IntegerField()
    annual_rent     = models.IntegerField(blank=True, null=True)
    annual_expense  = models.IntegerField(blank=True, null=True)
    purpose         = models.OneToOneField(LoanPurpose, on_delete=models.CASCADE, null=True)
    cash_out        = models.NullBooleanField(default=None)


class ClientRetailLoan(models.Model):
    client         = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    property_type  = models.CharField(max_length=25, default='', blank=True, null=True)
    name           = models.CharField(max_length=25, default='', blank=True, null=True)
    address        = models.CharField(max_length=25, default='', blank=True, null=True)
    annual_rent    = models.IntegerField(blank=True, null=True)
    annual_expense = models.IntegerField(blank=True, null=True)
    purpose        = models.OneToOneField(LoanPurpose, on_delete=models.CASCADE, null=True)
    cash_out       = models.NullBooleanField(default=None)


class LenderBLOCLoan(models.Model):
    lender     = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    resid_prop = models.BooleanField(default=False)
    stocks     = models.BooleanField(default=False)
    savings    = models.BooleanField(default=False)
    inv_prop   = models.BooleanField(default=False)
    pos1       = models.BooleanField(default=False)
    pos2       = models.BooleanField(default=False)


class LenderConstructionLoan(models.Model):
    lender         = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    renovation     = models.BooleanField(default=False)
    ground_up_spec = models.BooleanField(default=False)
    commercial     = models.BooleanField(default=False)
    residential    = models.BooleanField(default=False)
    inv_w_land     = models.BooleanField(default=False)
    oo_w_land      = models.BooleanField(default=False)


class LenderHELOCLoan(models.Model):
    lender = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    pos_1  = models.BooleanField(default=False)
    pos_2  = models.BooleanField(default=False)


class LenderMixedUseLoan(models.Model):
    lender = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)


class LenderMultiFamilyLoan(models.Model):
    lender  = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    mf_2to4 = models.BooleanField(default=False)
    mf_gt4  = models.BooleanField(default=False)


class LenderRetailLoan(models.Model):
    lender = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)


class LenderSBALoan(models.Model):
    lender  = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    sba_7a  = models.BooleanField(default=False)
    sba_504 = models.BooleanField(default=False)
    CAPline = models.BooleanField(default=False)
    micro   = models.BooleanField(default=False)
    other   = models.BooleanField(default=False)


class LenderBridgeLoan(models.Model):
    lender = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    bridge = models.BooleanField(default=False)


class LenderOwnerOccupiedRE(models.Model):
    lender        = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    office        = models.BooleanField(default=False)
    warehouse     = models.BooleanField(default=False)
    manufacturing = models.BooleanField(default=False)
    medical       = models.BooleanField(default=False)
    mixed_use     = models.BooleanField(default=False)
    other         = models.BooleanField(default=False)


class LenderInvestmentRE(models.Model):
    lender        = models.OneToOneField(Lender, on_delete=models.CASCADE, null=True)
    office        = models.BooleanField(default=False)
    warehouse     = models.BooleanField(default=False)
    manufacturing = models.BooleanField(default=False)
    medical       = models.BooleanField(default=False)
    mixed_use     = models.BooleanField(default=False)
    other         = models.BooleanField(default=False)

