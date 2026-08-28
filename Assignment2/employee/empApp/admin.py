from django.contrib import admin
from .models import Employees

class EmpAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','address','emp_id','phone','salary','dept')
    list_filter=('dept',)

admin.site.register(Employees,EmpAdmin)
