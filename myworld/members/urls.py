from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Student endpoints
    path("rest/student/<int:rolno>", views.StudentView.as_view()),
    path("rest/student/", views.StudentView.as_view()),
    path("rest/student/<str:branch>", views.StudentView.as_view()),
    # Employee endpoints
    path("rest/employee/<int:emp_id>", views.EmployeeView.as_view()),
    path("rest/employee/", views.EmployeeView.as_view()),
    # Blog endpoints
    path("start_python_blog_scraping", views.python_blog_scrap, name="triger"),
    path("rest/blog/", views.BlogView.as_view()),
]
