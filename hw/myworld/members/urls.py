from django.urls import path
from . import views

urlpatterns = [
    path('rest/e/<int:eid>', views.EmployeeView.as_view()),
    path('rest/e/', views.EmployeeView.as_view()),
    path('rest/e/<str:branch>', views.EmployeeView.as_view()),
]
