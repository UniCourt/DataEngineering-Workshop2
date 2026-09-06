from django.contrib import admin

from .models import Blog, Employee, Students


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
    list_display = (
        "title",
        "author",
        "release_date",
        "blog_time",
        "total_comments",
        "recommended_google",
        "created_date",
    )
    list_filter = ("author", "release_date")


class DjEmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "emp_id",
        "first_name",
        "last_name",
        "email",
        "department",
        "salary",
    )
    list_filter = ("department",)


# Register your models here.
admin.site.register(Students, DjStudentAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Employee, DjEmployeeAdmin)

