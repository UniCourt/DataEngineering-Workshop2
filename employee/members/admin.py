from django.contrib import admin
from .models import Employee

class DjEmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "emp_id", "mobile", "department","salary")
    list_filter = ("department",)

# Register your models here.
admin.site.register(Employee, DjEmployeeAdmin) 