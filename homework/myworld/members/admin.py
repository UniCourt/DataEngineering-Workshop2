from django.contrib import admin
from .models import Emp, Blog

class DjStudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "address", "empid", "salary", "mobile", "branch")
    list_filter = ("empid",)
class DjBlogAdmin(admin.ModelAdmin):
  list_display = ("title", "release_date", "blog_time", "author", "created_date", "content", "recommended", "path")
  list_filter = ("author",)
  
# Register your models here.
admin.site.register(Blog, DjBlogAdmin)
admin.site.register(Emp, DjStudentAdmin) 

