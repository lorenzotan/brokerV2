from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def register(req):
    tmpl = loader.get_template('accounts/register.html')
    return HttpResponse(tmpl.render())


def login(req):
    tmpl = loader.get_template('accounts/login.html')
    return HttpResponse(tmpl.render())
