from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(req):
    tmpl = loader.get_template('home/index.html')

    attr = {}

    return HttpResponse(tmpl.render(attr, req))

def denied(req):
    #template = loader.get_template('home/index.html')
    return render_to_response('home/denied.html')

