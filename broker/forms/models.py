from django.db import models
from django.core.validators import RegexValidator

#NOTE: Meta options: https://docs.djangoproject.com/en/dev/ref/models/options/

# Create your models here.
class Qualifiers(models.Model):
    name = models.CharField(max_length=50, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LoanTypes(models.Model):
    name  = models.CharField(max_length=50, default=None, null=True, blank=True)
    model = models.CharField(max_length=50, default=None, null=True, blank=True)
    form  = models.CharField(max_length=50, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
    

class PropertyTypes(models.Model):
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


class PointOfContact(models.Model):
    first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    last_name  = models.CharField(max_length=50, default=None, null=True, blank=True)
    company    = models.CharField(max_length=100, default=None, null=True, blank=True)
    w_email    = models.EmailField(max_length=100, default=None, null=True, blank=True)
    m_phone    = models.CharField(max_length=10, blank=True)
    w_phone    = models.CharField(max_length=10, blank=True)


class ClientBusinessInfo(models.Model):
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
    amount   = models.DecimalField(max_digits=17, decimal_places=2)
    loan2val = models.DecimalField(max_digits=17, decimal_places=2)
    dscr     = models.DecimalField(max_digits=17, decimal_places=2)
    desc     = models.TextField()


class ClientFinancialInfo(models.Model):
    salary        = models.DecimalField(max_digits=17, decimal_places=2)
    yrs_in_biz    = models.PositiveSmallIntegerField()
    debt          = models.DecimalField(max_digits=17, decimal_places=2)
    mnthly_pymnts = models.DecimalField(max_digits=17, decimal_places=2)
    fico          = models.PositiveSmallIntegerField()
    owns_home     = models.BooleanField()
    bankruptcy    = models.BooleanField()
    short_sale    = models.BooleanField()


class ClientPropertyInfo(models.Model):
    address = models.CharField(max_length=50, default=None, null=True, blank=True)
    value   = models.DecimalField(max_digits=17, decimal_places=2)


class Clients(models.Model):
    first_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    last_name  = models.CharField(max_length=50, default=None, null=True, blank=True)
    address    = models.CharField(max_length=50, default=None, null=True, blank=True)
    city       = models.CharField(max_length=50, default=None, null=True, blank=True)
    state      = models.CharField(max_length=2, default=None, null=True, blank=True)
    zip_code   = models.CharField(max_length=10, default=None, null=True, blank=True)
    h_email    = models.EmailField(max_length=100, default=None, null=True, blank=True)
    w_email    = models.EmailField(max_length=100, default=None, null=True, blank=True)
    # NOTE https://github.com/VeryApt/django-phone-field
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    h_phone    = models.CharField(max_length=10, blank=True)
    w_phone    = models.CharField(max_length=10, blank=True)
    loantype   = models.ForeignKey(LoanTypes, on_delete=models.SET_NULL, blank=True, null=True)
    poc        = models.ManyToManyField(PointOfContact)
    business   = models.ForeignKey(ClientBusinessInfo, on_delete=models.SET_NULL, blank=True, null=True)
    qualifers  = models.ManyToManyField(Qualifiers)
    needslist  = models.ManyToManyField(NeedsList)


class Lenders(models.Model):
    first_name    = models.CharField(max_length=50, default=None, null=True, blank=True)
    last_name     = models.CharField(max_length=50, default=None, null=True, blank=True)
    company       = models.CharField(max_length=100, default=None, null=True, blank=True)
    address       = models.CharField(max_length=50, default=None, null=True, blank=True)
    city          = models.CharField(max_length=50, default=None, null=True, blank=True)
    state         = models.CharField(max_length=2, default=None, null=True, blank=True)
    zip_code      = models.CharField(max_length=10, default=None, null=True, blank=True)
    h_email       = models.EmailField(max_length=100, default=None, null=True, blank=True)
    w_email       = models.EmailField(max_length=100, default=None, null=True, blank=True)
    h_phone       = models.CharField(max_length=10, blank=True)
    w_phone       = models.CharField(max_length=10, blank=True)
    solicitation  = models.BooleanField()
    qualifers     = models.ManyToManyField(Qualifiers)
    propertytypes = models.ManyToManyField(PropertyTypes)

