from django.contrib import admin
from .models import Students
from .models import Employee

class DjStudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "roll_number", "mobile", "branch")
    list_filter = ("branch",)

class DjEmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "emp_id", "mobile", "role","salary")
    list_filter = ("role",)

# Register your models here.
admin.site.register(Students, DjStudentAdmin)
admin.site.register(Employee, DjEmployeeAdmin)