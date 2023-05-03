from django.contrib import admin
from .models import Employees

class EmpAdmin(admin.ModelAdmin):
    list_display = ('emp_id','name','address','salary','dept')
    list_filter=('dept',)

admin.site.register(Employees,EmpAdmin)
