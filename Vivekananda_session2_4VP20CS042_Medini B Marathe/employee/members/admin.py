from django.contrib import admin
from .models import Emp

class DjStudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "empid", "salary", "mobile", "branch")
    list_filter = ("empid",)

# Register your models here.
admin.site.register(Emp, DjStudentAdmin) 
