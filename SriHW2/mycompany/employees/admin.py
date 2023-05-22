from django.contrib import admin
from .models import Employees

class DjEmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "emp_id", "address", "mobile", "dept","salary",)
    list_filter = ("dept",)

# Register your models here.
admin.site.register(Employees, DjEmployeeAdmin)
