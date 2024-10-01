from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('employeeapp/', include('employeeapp.urls')),
    path('admin/', admin.site.urls),
]