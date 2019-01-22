from django.urls import path, re_path

from . import views

app_name = 'loans'
urlpatterns = [
    re_path('lender/(?P<pk>[0-9]+)/$', views.lender_detail, name='lender_detail'),
    re_path('lender_form/(?P<pk>[0-9]+)/$', views.edit_lender_form, name='edit_lender_form'),
    path('lender_form/', views.lender_form, name='lender_form'),
    path('lender_list/', views.lender_list, name='lenders'),

    #re_path('loan/(?P<pk>[0-9]+)/$', views.lender_detail, name='lender_detail'),
    #re_path('loan_form/(?P<pk>[0-9]+)/$', views.edit_lender_form, name='edit_lender_form'),
    path('loan_form/', views.loan_form, name='loan_form'),
    path('loan_list/', views.loan_list, name='loan_list'),
]
