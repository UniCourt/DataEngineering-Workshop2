from django.urls import path
from . import views

urlpatterns = [
    path('v1/employees/<int:eid>', views.EmployeesView.as_view()),
    path('v1/employees/', views.EmployeesView.as_view()),
]