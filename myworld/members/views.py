from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Students, Employee


def index(request):
    """Morning Hello World page used by /members/."""
    template = loader.get_template("myfirst.html")
    return HttpResponse(template.render())


@method_decorator(csrf_exempt, name="dispatch")
class StudentView(View):
    """Homework REST endpoints for Students (optional after class)."""

    def get(self, request, rolno=None, branch=None):
        student_model_list = []
        try:
            if rolno:
                student_model_list = Students.objects.filter(roll_number=rolno)
            elif branch:
                student_model_list = Students.objects.filter(branch=branch)
        except Students.DoesNotExist:
            return JsonResponse(
                {"status": "failed", "students": None}, status=400
            )
        students = []
        for student in student_model_list:
            data = {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "address": student.address,
                "roll_number": student.roll_number,
                "mobile": student.mobile,
                "branch": student.branch,
            }
            students.append(data)
        return JsonResponse(
            {"status": "success", "students": students}, status=200
        )

    def post(self, request):
        if (
            not request.POST.get("first_name")
            or not request.POST.get("last_name")
            or not request.POST.get("address")
            or not request.POST.get("roll_number")
            or not request.POST.get("mobile")
        ):
            return JsonResponse(
                {"status": "failed", "message": "all fields required"},
                status=500,
            )

        Students.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            address=request.POST.get("address"),
            roll_number=request.POST.get("roll_number"),
            mobile=request.POST.get("mobile"),
            branch=request.POST.get("branch"),
        )
        return JsonResponse({"status": "success"}, status=200)

@csrf_exempt
def add_employee(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": "failed",
                "message": "POST method required"
            },
            status=405
        )

    emp_id = request.POST.get("emp_id")
    name = request.POST.get("name")
    email = request.POST.get("email")
    department = request.POST.get("department")
    salary = request.POST.get("salary")

    if not all([emp_id, name, email, department, salary]):
        return JsonResponse(
            {
                "status": "failed",
                "message": "All fields are required"
            },
            status=400
        )

    try:
        employee = Employee.objects.create(
            emp_id=emp_id,
            name=name,
            email=email,
            department=department,
            salary=salary
        )

        return JsonResponse(
            {
                "status": "success",
                "message": "Employee added successfully",
                "employee": {
                    "emp_id": employee.emp_id,
                    "name": employee.name,
                    "email": employee.email,
                    "department": employee.department,
                    "salary": str(employee.salary)
                }
            },
            status=201
        )

    except Exception as e:
        return JsonResponse(
            {
                "status": "failed",
                "message": str(e)
            },
            status=400
        )

def get_employee(request, emp_id):
    if request.method != "GET":
        return JsonResponse(
            {
                "status": "failed",
                "message": "GET method required"
            },
            status=405
        )

    try:
        employee = Employee.objects.get(emp_id=emp_id)

        return JsonResponse(
            {
                "status": "success",
                "employee": {
                    "emp_id": employee.emp_id,
                    "name": employee.name,
                    "email": employee.email,
                    "department": employee.department,
                    "salary": str(employee.salary)
                }
            },
            status=200
        )

    except Employee.DoesNotExist:
        return JsonResponse(
            {
                "status": "failed",
                "message": "Employee not found"
            },
            status=404
        )

@csrf_exempt
def delete_employee(request, emp_id):
    if request.method != "DELETE":
        return JsonResponse(
            {
                "status": "failed",
                "message": "DELETE method required"
            },
            status=405
        )

    try:
        employee = Employee.objects.get(emp_id=emp_id)
        employee.delete()

        return JsonResponse(
            {
                "status": "success",
                "message": "Employee deleted successfully"
            },
            status=200
        )

    except Employee.DoesNotExist:
        return JsonResponse(
            {
                "status": "failed",
                "message": "Employee not found"
            },
            status=404
        )

@csrf_exempt
def update_employee_salary(request, emp_id):
    if request.method != "PUT":
        return JsonResponse(
            {
                "status": "failed",
                "message": "PUT method required"
            },
            status=405
        )

    try:
        import json

        data = json.loads(request.body)
        salary = data.get("salary")

        if salary is None:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": "Salary is required"
                },
                status=400
            )

        employee = Employee.objects.get(emp_id=emp_id)
        employee.salary = salary
        employee.save()

        return JsonResponse(
            {
                "status": "success",
                "message": "Employee salary updated successfully",
                "employee": {
                    "emp_id": employee.emp_id,
                    "name": employee.name,
                    "salary": str(employee.salary)
                }
            },
            status=200
        )

    except Employee.DoesNotExist:
        return JsonResponse(
            {
                "status": "failed",
                "message": "Employee not found"
            },
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {
                "status": "failed",
                "message": str(e)
            },
            status=400
        )
