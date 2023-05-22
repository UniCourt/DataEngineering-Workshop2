from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())
