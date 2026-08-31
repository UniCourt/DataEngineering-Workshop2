
from django.contrib import admin

from .models import Blog, Students, Employee


class DjStudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "address",
        "roll_number",
        "mobile",
        "branch",
    )
    list_filter = ("branch",)


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "release_date", "blog_time", "created_date")
    list_filter = ("author",)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "emp_id",
        "name",
        "email",
        "department",
        "salary",
    )
    list_filter = ("department",)
    search_fields = ("emp_id", "name", "email")

# Register your models here.
admin.site.register(Students, DjStudentAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Employee, EmployeeAdmin)
