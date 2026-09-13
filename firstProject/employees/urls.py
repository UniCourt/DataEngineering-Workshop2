from django.urls import path

from . import views

urlpatterns = [
    path("", views.employee_admin_view, name="employee_admin_view"),
    path("api/add/", views.add_employee, name="add_employee"),
    path("api/<int:emp_id>/", views.get_employee, name="get_employee"),
    path("api/<int:emp_id>/delete/", views.delete_employee, name="delete_employee"),
    path(
        "api/<int:emp_id>/salary/",
        views.update_employee_salary,
        name="update_employee_salary",
    ),
]
