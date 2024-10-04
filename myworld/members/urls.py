from django.urls import path
from . import views

urlpatterns = [
    path('rest/student/<int:rolno>/', views.StudentView.as_view()),  
    path('rest/student/', views.StudentView.as_view()),               
    path('rest/student/branch/<str:branch>/', views.StudentView.as_view()),  # For specific branch
    path('rest/employee/<int:emp_id>/', views.EmployeeView.as_view()),  
    path('rest/employee/', views.EmployeeView.as_view())               
]
