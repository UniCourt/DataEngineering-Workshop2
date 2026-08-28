from django.contrib import admin
from .models import Members

class PersonAdmin(admin.ModelAdmin):
    list_display = ('Employeename', 'EmployeeId','Salary')

admin.site.register(Members,PersonAdmin)
# Register your models here.
