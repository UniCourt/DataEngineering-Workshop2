from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rest/student/<int:rolno>', views.StudentView.as_view()),
    path('rest/student/', views.StudentView.as_view()),
    path('rest/student/<str:branch>', views.StudentView.as_view()),
    path('rest/student/<int:rolno>', views.StudentView.as_view()),
    path('rest/student/', views.StudentView.as_view()),
    path('rest/student/<str:branch>', views.StudentView.as_view()),
    path('start_python_blog_scraping', views.python_blog_scrap, name='triger'),
    path('rest/student/<int:rolno>', views.StudentView.as_view()),
    path('rest/student/', views.StudentView.as_view()),
    path('rest/student/<str:branch>', views.StudentView.as_view()),
    path('start_python_blog_scraping', views.python_blog_scrap, name='triger'),
    path('rest/blog/', views.BlogView.as_view())
]

