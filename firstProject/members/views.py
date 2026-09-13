from django.shortcuts import render
from .models import Members

def index(request):
    members = Members.objects.all()
    return render(request, 'myfirst.html', {'members': members})