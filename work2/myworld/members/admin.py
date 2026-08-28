from django.contrib import admin
from .models import Employees

class DjEmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "emp_id", "salary", "department")
    list_filter = ("department",)

# Register your models here.
admin.site.register(Employees, DjEmployeeAdmin) 
