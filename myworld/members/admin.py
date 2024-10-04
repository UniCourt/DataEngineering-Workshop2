from django.contrib import admin
from .models import Students

class DjStudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "roll_number", "mobile", "branch")
    list_filter = ("branch",)

# Register your models here.
admin.site.register(Students, DjStudentAdmin) 