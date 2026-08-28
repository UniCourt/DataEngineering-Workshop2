from django.urls import path
from . import views

urlpatterns = [
    path('rest/employee/<int:empid>', views.EmployeeView.as_view()),
    path('rest/employee/', views.EmployeeView.as_view()),
    path('rest/employee/<str:department>', views.EmployeeView.as_view()),
]
