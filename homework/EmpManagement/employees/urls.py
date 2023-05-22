from django.urls import path
from . import views

urlpatterns = [
    path('employee/<int:emp_id>', views.EmployeeView.as_view()),
    path('employee/', views.EmployeeView.as_view()),
    path('employee/<str:dept>', views.EmployeeView.as_view()),
]