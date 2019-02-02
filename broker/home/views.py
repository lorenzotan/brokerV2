from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(req):
# SCENARIOS
# 1. if user is logged in
#    A. if user has a group
#    B. if user has NO group
# 2. if user is not logged in
    tmpl = loader.get_template('home/index.html')

    attr = {}

    return HttpResponse(tmpl.render(attr, req))

def denied(req):
    #template = loader.get_template('home/index.html')
    return render_to_response('home/denied.html')

