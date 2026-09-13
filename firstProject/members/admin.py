from django.contrib import admin
from .models import Members,Blog

class PersonAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')

admin.site.register(Members,PersonAdmin)
admin.site.register(Blog)
# Register your models here.