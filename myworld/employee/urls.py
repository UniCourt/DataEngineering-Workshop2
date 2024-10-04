from django.urls import path
from .views import EmployeeView

urlpatterns = [
    path('employee/', EmployeeView.as_view(), name='employee_list'),
    path('employee/<int:emp_id>/', EmployeeView.as_view(), name='employee_detail'),
]
