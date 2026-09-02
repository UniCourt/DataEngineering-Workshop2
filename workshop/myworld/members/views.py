from django.http import HttpResponse
from django.template import loader

# New homepage view
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

# Existing members view
def index(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())
