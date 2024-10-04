from django.contrib import admin
from .models import Students
from .models import Employees

class DjStudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "roll_number", "mobile", "branch")
    list_filter = ("branch",)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "emp_id" , "salary")
    
# Register your models here.
admin.site.register(Students, DjStudentAdmin)
admin.site.register(Employees,EmployeeAdmin)