from django.contrib import admin
from .models import Members

class PersonAdmin(admin.ModelAdmin):
    list_display = ('EmployeeId','Employeename','Salary','companyname')

admin.site.register(Members,PersonAdmin)




