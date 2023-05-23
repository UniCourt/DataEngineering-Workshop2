from django.contrib import admin

from .models import Employees

class DjEmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "employee_salary", "employee_id", "mobile")
    #list_filter = ("employee_id")

# Register your models here.
admin.site.register(Employees, DjEmployeeAdmin) 
