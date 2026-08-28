from django.contrib import admin
from .models import Employee 

class DjEmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "emp_id", "address", "mobile", "dept","salary",)
    list_filter = ("dept",)


admin.site.register(Employee, DjEmployeeAdmin)
