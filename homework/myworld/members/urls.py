from django.urls import path
from . import views

urlpatterns = [
    path('rest/e/<int:eid>', views.EmployeeView.as_view()),
    path('rest/e/', views.EmployeeView.as_view()),
    path('rest/e/<str:branch>', views.EmployeeView.as_view()),
    path('start_python_blog_scraping', views.python_blog_scrap, name='triger'),
    path('rest/blog/', views.BlogView.as_view())
]
