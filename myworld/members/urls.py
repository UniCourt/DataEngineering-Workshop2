from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),

    path("rest/student/<int:rolno>", views.StudentView.as_view()),
    path("rest/student/", views.StudentView.as_view()),
    path("rest/student/<str:branch>", views.StudentView.as_view()),

    path(
        "api/employees",
        views.add_employee,
        name="add_employee"
    ),

    path(
        "api/employees/<int:emp_id>",
        views.get_employee,
        name="get_employee"
    ),
   path(
    "api/employees/<int:emp_id>/delete",
    views.delete_employee,
    name="delete_employee"
),
path(
    "api/employees/<int:emp_id>/salary",
    views.update_employee_salary,
    name="update_employee_salary"
),	
]
