from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('select_group/', views.select_group, name='select_group'),
    #path('register/', views.Register.as_view(), name='register'),
]
