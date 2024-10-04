from django.views import View
from .models import Students,Employee
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json



@method_decorator(csrf_exempt, name='dispatch')
class StudentView(View):

    def get(self, request, rolno=None, branch=None):
        student_model_list = []
        try:
            if rolno:
                student_model_list = Students.objects.filter(roll_number=rolno)
            elif branch:
                student_model_list = Students.objects.filter(branch=branch)
        except Students.DoesNotExist:
            return JsonResponse({'status': 'failed', "students": None}, status=400)
        students = []
        for student in student_model_list:
            data = {
                "first_name" : student.first_name,
                "last_name": student.last_name,
                "address": student.address,
                "roll_number": student.roll_number,
                "mobile": student.mobile,
                "branch": student.branch
            }
            students.append(data)
        return JsonResponse({'status': 'success', "students": students}, status=200)

    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or  not request.POST.get('roll_number') or not request.POST.get('mobile'):
            return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)

        Students.objects.create(
            first_name= request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            address= request.POST.get('address'),
            roll_number= request.POST.get('roll_number'),
            mobile= request.POST.get('mobile'),
            branch= request.POST.get('branch'))
        return JsonResponse({'status': 'sucess'}, status=200)
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):
    def get(self, request, emp_id=None, role=None):
        employee_model_list = []
        if emp_id:
            employee_model_list = Employee.objects.filter(emp_id=emp_id)
        elif role:
            employee_model_list = Employee.objects.filter(role=role)
        else:
            employee_model_list = Employee.objects.all()

        employees = [
            {
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "address": emp.address,
                "emp_id": emp.emp_id,
                "salary": emp.salary,
                "mobile": emp.mobile,
                "role": emp.role
            }
            for emp in employee_model_list
        ]

        return JsonResponse({'status': 'success', "employees": employees}, status=200)

    def post(self, request):
        data = json.loads(request.body)  # Expecting JSON data
        required_fields = ['first_name', 'last_name', 'address', 'emp_id', 'mobile', 'role']

        if not all(data.get(field) for field in required_fields):
            return JsonResponse({'status': 'failed', "message": "all fields required"}, status=400)

        Employee.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            emp_id=data['emp_id'],
            salary=data.get('salary'),
            mobile=data['mobile'],
            role=data['role']
        )
        return JsonResponse({'status': 'success'}, status=201)

    def delete(self, request, emp_id):
        try:
            employee = Employee.objects.get(emp_id=emp_id)
            employee.delete()
            return JsonResponse({'status': 'success', 'message': 'Employee deleted.'}, status=204)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found.'}, status=404)

    def put(self, request, emp_id):
        data = json.loads(request.body)  # Expecting JSON data
        try:
            employee = Employee.objects.get(emp_id=emp_id)
            if 'salary' in data:
                employee.salary = data['salary']
            employee.save()
            return JsonResponse({'status': 'success', 'message': 'Employee updated.'}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found.'}, status=404)
