from django.contrib import admin
from .models import Employees

# Register your models here.
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "emp_id", "mobile", "department")

# Register your models here.
admin.site.register(Employees, EmployeesAdmin)