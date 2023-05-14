from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rest/student/<int:rolno>', views.StudentView.as_view()),
    path('rest/student/', views.StudentView.as_view()),
    path('rest/student/<str:branch>', views.StudentView.as_view()),
]
