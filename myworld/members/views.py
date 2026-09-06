import json
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import apps
from .models import Blog, Employee, Students


def index(request):
    """Morning Hello World page used by /members/."""
    template = loader.get_template("myfirst.html")
    return HttpResponse(template.render())


@method_decorator(csrf_exempt, name="dispatch")
class StudentView(View):
    """Homework REST endpoints for Students."""

    def get(self, request, rolno=None, branch=None):
        student_model_list = []
        try:
            if rolno:
                student_model_list = Students.objects.filter(roll_number=rolno)
            elif branch:
                student_model_list = Students.objects.filter(branch=branch)
            else:
                student_model_list = Students.objects.all()
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
                status=400,
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


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeView(View):
    """REST API endpoints for Employee model: Create, Read, Update salary, Delete."""

    def get(self, request, emp_id=None):
        if emp_id:
            try:
                emp = Employee.objects.get(emp_id=emp_id)
                data = {
                    "emp_id": emp.emp_id,
                    "first_name": emp.first_name,
                    "last_name": emp.last_name,
                    "email": emp.email,
                    "department": emp.department,
                    "salary": str(emp.salary),
                }
                return JsonResponse({"status": "success", "employee": data}, status=200)
            except Employee.DoesNotExist:
                return JsonResponse(
                    {"status": "failed", "message": "Employee not found"}, status=404
                )
        else:
            employees = list(
                Employee.objects.values(
                    "emp_id", "first_name", "last_name", "email", "department", "salary"
                )
            )
            for emp in employees:
                emp["salary"] = str(emp["salary"])
            return JsonResponse({"status": "success", "employees": employees}, status=200)

    def post(self, request):
        data = request.POST
        if not data and request.body:
            try:
                data = json.loads(request.body)
            except Exception:
                data = {}

        emp_id = data.get("emp_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email", "")
        department = data.get("department", "")
        salary = data.get("salary", 0.00)

        if not emp_id or not first_name or not last_name:
            return JsonResponse(
                {"status": "failed", "message": "emp_id, first_name and last_name are required"},
                status=400,
            )

        if Employee.objects.filter(emp_id=emp_id).exists():
            return JsonResponse(
                {"status": "failed", "message": f"Employee with emp_id {emp_id} already exists"},
                status=400,
            )

        emp = Employee.objects.create(
            emp_id=emp_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            salary=salary,
        )
        return JsonResponse(
            {
                "status": "success",
                "message": "Employee added successfully",
                "emp_id": emp.emp_id,
            },
            status=201,
        )

    def put(self, request, emp_id=None):
        return self.update_salary(request, emp_id)

    def patch(self, request, emp_id=None):
        return self.update_salary(request, emp_id)

    def update_salary(self, request, emp_id):
        if not emp_id:
            return JsonResponse(
                {"status": "failed", "message": "emp_id is required"}, status=400
            )

        try:
            emp = Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            return JsonResponse(
                {"status": "failed", "message": "Employee not found"}, status=404
            )

        data = {}
        if request.body:
            try:
                data = json.loads(request.body)
            except Exception:
                pass
        if not data:
            data = request.POST

        salary = data.get("salary")
        if salary is None:
            return JsonResponse(
                {"status": "failed", "message": "salary field is required"}, status=400
            )

        emp.salary = salary
        emp.save()
        return JsonResponse(
            {
                "status": "success",
                "message": f"Employee {emp_id} salary updated successfully",
                "salary": str(emp.salary),
            },
            status=200,
        )

    def delete(self, request, emp_id=None):
        if not emp_id:
            return JsonResponse(
                {"status": "failed", "message": "emp_id is required"}, status=400
            )

        try:
            emp = Employee.objects.get(emp_id=emp_id)
            emp.delete()
            return JsonResponse(
                {"status": "success", "message": f"Employee {emp_id} deleted successfully"},
                status=200,
            )
        except Employee.DoesNotExist:
            return JsonResponse(
                {"status": "failed", "message": "Employee not found"}, status=404
            )


@method_decorator(csrf_exempt, name="dispatch")
class BlogView(View):
    """REST API endpoints for Blog scraper and retrieval."""

    def get(self, request):
        blog_model_list = Blog.objects.all()
        blogs = []
        for blog in blog_model_list:
            data = {
                "Title": blog.title,
                "Release Date": str(blog.release_date) if blog.release_date else "",
                "Author": blog.author,
                "Blog time": blog.blog_time,
                "Total Comments": blog.total_comments,
                "Recommended Count": blog.recommended_google,
                "HTML File Path": blog.html_file_path,
            }
            blogs.append(data)
        return JsonResponse({"status": "success", "blogs": blogs}, status=200)

    def post(self, request):
        start_date = request.POST.get("start_date", None)
        end_date = request.POST.get("end_date", None)
        no_of_articles = request.POST.get("no_of_articles", None)
        start_id = request.POST.get("start_id", None)

        if not request.POST and request.body:
            try:
                body_data = json.loads(request.body)
                start_date = body_data.get("start_date", start_date)
                end_date = body_data.get("end_date", end_date)
                no_of_articles = body_data.get("no_of_articles", no_of_articles)
                start_id = body_data.get("start_id", start_id)
            except Exception:
                pass

        apps.start_extraction(
            start_date=start_date,
            end_date=end_date,
            no_of_articles=no_of_articles,
            start_id=start_id,
        )

        blog_model_list = Blog.objects.all()
        blogs = []
        for blog in blog_model_list:
            data = {
                "Title": blog.title,
                "Release Date": str(blog.release_date) if blog.release_date else "",
                "Author": blog.author,
                "Blog time": blog.blog_time,
                "Total Comments": blog.total_comments,
                "Recommended Count": blog.recommended_google,
                "HTML File Path": blog.html_file_path,
            }
            blogs.append(data)

        return JsonResponse({"status": "success", "blogs": blogs}, status=200)


@csrf_exempt
def python_blog_scrap(request):
    """View to trigger Python blog scraping."""
    apps.start_extraction()
    return JsonResponse(
        {"status": "sucess", "message": "Extracted and populated the table."}, status=200
    )
