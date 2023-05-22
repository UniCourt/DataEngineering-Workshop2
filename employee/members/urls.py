from django.urls import path
from . import views

urlpatterns = [
    path('rest/employee/<int:employee_id>', views.EmployeeView.as_view()),
    path('rest/employee/<int:empid>', views.EmployeeView.as_view()),
    path('rest/employee/', views.EmployeeView.as_view()),
    path('rest/employee/<int:employee_id><int:employee_salary>',views.EmployeeView.as_view()),
    path('', views.index, name='index')
]
