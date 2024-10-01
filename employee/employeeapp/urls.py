from django.urls import path
from .views import EmployeeView

urlpatterns = [
    path('rest/employee/id/<int:empid>', EmployeeView.as_view()),  
    path('rest/employee/', EmployeeView.as_view()),  
    path('rest/employee/department/<str:department>', EmployeeView.as_view()),  
]