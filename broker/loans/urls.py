from django.urls import path, re_path

from . import views

app_name = 'loans'
urlpatterns = [
    re_path('lender/(?P<pk>[0-9]+)/$', views.lender_detail, name='lender_detail'),
    re_path('lender_form/(?P<pk>[0-9]+)/$', views.edit_lender_form, name='edit_lender_form'),
    path('lender_form/', views.lender_form, name='lender_form'),
    path('lender_list/', views.lender_list, name='lenders'),

    re_path('broker/(?P<pk>[0-9]+)/$', views.broker_detail, name='broker_detail'),
    re_path('broker_form/(?P<pk>[0-9]+)/$', views.edit_broker_form, name='edit_broker_form'),
    path('broker_form/', views.broker_form, name='broker_form'),
    path('broker_list/', views.broker_list, name='brokers'),

    #re_path('client/(?P<pk>[0-9]+)/$', views.client, name='client_detail'),
    #re_path('client_form/(?P<pk>[0-9]+)/$', views.edit_client_form, name='edit_client_form'),
    #path('loan_form/', views.loan_form, name='loan_form'),
    #path('loan_list/', views.loan_list, name='loan_list'),
]
