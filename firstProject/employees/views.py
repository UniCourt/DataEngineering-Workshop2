import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Employee


def employee_admin_view(request):
    """
    Simple read-only page listing all saved employees.
    Complements Django's built-in /admin/ (which also lists Employees).
    """
    employees = Employee.objects.all().order_by("emp_id")
    return render(request, "employee_list.html", {"employees": employees})


@csrf_exempt
@require_http_methods(["POST"])
def add_employee(request):
    """POST /employees/api/add/  body: {"name", "email", "salary", "department"?}"""
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    name = data.get("name")
    email = data.get("email")
    salary = data.get("salary")
    department = data.get("department", "")

    if not name or not email or salary is None:
        return JsonResponse(
            {"error": "name, email and salary are required"}, status=400
        )

    if Employee.objects.filter(email=email).exists():
        return JsonResponse(
            {"error": "An employee with this email already exists"}, status=409
        )

    employee = Employee(name=name, email=email, salary=salary, department=department)
    try:
        employee.full_clean()
        employee.save()
    except ValidationError as e:
        return JsonResponse({"error": e.message_dict}, status=400)

    return JsonResponse(
        {"message": "Employee created", "employee": employee.to_dict()}, status=201
    )


@require_http_methods(["GET"])
def get_employee(request, emp_id):
    """GET /employees/api/<emp_id>/"""
    try:
        employee = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse(
            {"error": f"Employee with emp_id {emp_id} not found"}, status=404
        )

    return JsonResponse({"employee": employee.to_dict()}, status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_employee(request, emp_id):
    """DELETE /employees/api/<emp_id>/delete/"""
    try:
        employee = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse(
            {"error": f"Employee with emp_id {emp_id} not found"}, status=404
        )

    employee.delete()
    return JsonResponse({"message": f"Employee {emp_id} deleted"}, status=200)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_employee_salary(request, emp_id):
    """PUT/PATCH /employees/api/<emp_id>/salary/  body: {"salary": 55000}"""
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    salary = data.get("salary")
    if salary is None:
        return JsonResponse({"error": "salary is required"}, status=400)

    try:
        employee = Employee.objects.get(emp_id=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse(
            {"error": f"Employee with emp_id {emp_id} not found"}, status=404
        )

    employee.salary = salary
    try:
        employee.full_clean()
        employee.save()
    except ValidationError as e:
        return JsonResponse({"error": e.message_dict}, status=400)

    return JsonResponse(
        {"message": "Salary updated", "employee": employee.to_dict()}, status=200
    )
