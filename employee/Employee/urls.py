from django.urls import path
from . import views

urlpatterns = [
    path('rest/employee/<int:emp_id>', views.EmployeeView.as_view()),
    path('rest/employee/', views.EmployeeView.as_view()),
    path('rest/employee/<str:dept>', views.EmployeeView.as_view()),
]
