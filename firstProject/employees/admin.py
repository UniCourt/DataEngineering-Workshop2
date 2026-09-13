from django.contrib import admin

from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_id", "name", "email", "department", "salary", "updated_at")
    search_fields = ("name", "email", "department")
    list_filter = ("department",)


admin.site.register(Employee, EmployeeAdmin)
