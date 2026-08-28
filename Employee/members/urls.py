from django.urls import path
from . import views

urlpatterns = [
    path('rest/employee/<int:emp_id>/', views.EmployeeView.as_view(), name='employee_by_id'),
    path('rest/employee/', views.EmployeeView.as_view(), name='employee_list'),
    path('rest/employee/department/<str:department>/', views.EmployeeView.as_view(), name='employee_by_department'),
]
