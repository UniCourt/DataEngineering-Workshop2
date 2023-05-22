from django.urls import path
from . import views

urlpatterns = [
    path('employees/<int:emp_id>', views.EmployeeView.as_view()),
    path('employees/', views.EmployeeView.as_view()),
    path('employees/<str:dept>', views.EmployeeView.as_view()),
]
