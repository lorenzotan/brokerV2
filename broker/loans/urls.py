from django.urls import path

from . import views

app_name = 'loans'
urlpatterns = [
    path('lender_form/', views.lender_form, name='lender_form'),
    path('lender_list/', views.lender_list, name='lender_list'),
    path('loan_form/', views.loan_form, name='loan_form'),
    path('loan_list/', views.loan_list, name='loan_list'),
]
