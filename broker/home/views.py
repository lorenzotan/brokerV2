from django.shortcuts import render, render_to_response
from django.template import loader

# Create your views here.
def index(req):
    #template = loader.get_template('home/index.html')
    return render_to_response('home/index.html')

