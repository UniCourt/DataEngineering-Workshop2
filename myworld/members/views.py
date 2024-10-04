import json
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Students, Employees

# View to handle Students API
@method_decorator(csrf_exempt, name='dispatch')
class StudentView(View):

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
            return JsonResponse({'status': 'failed', "students": None}, status=400)

        students = []
        for student in student_model_list:
            data = {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "address": student.address,
                "roll_number": student.roll_number,
                "mobile": student.mobile,
                "branch": student.branch
            }
            students.append(data)
        
        return JsonResponse({'status': 'success', "students": students}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            required_fields = ['first_name', 'last_name', 'address', 'roll_number', 'mobile']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'status': 'failed', "message": f"{field} is required"}, status=500)

            Students.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                address=data.get('address'),
                roll_number=data.get('roll_number'),
                mobile=data.get('mobile'),
                branch=data.get('branch')
            )
            return JsonResponse({'status': 'success', 'message': 'Student added successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', "message": "Invalid JSON data"}, status=400)


# View to handle Employees API
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):

    def get(self, request, emp_id=None):
        employee_list = []
        try:
            if emp_id:
                employee_list = Employees.objects.filter(emp_id=emp_id)
            else:
                employee_list = Employees.objects.all()
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "employees": None}, status=400)

        employees = []
        for employee in employee_list:
            data = {
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "address": employee.address,
                "emp_id": employee.emp_id,
                "salary": employee.salary
            }
            employees.append(data)

        return JsonResponse({'status': 'success', "employees": employees}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            required_fields = ['first_name', 'last_name', 'address', 'emp_id', 'salary']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'status': 'failed', "message": f"{field} is required"}, status=500)

            Employees.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                address=data.get('address'),
                emp_id=data.get('emp_id'),
                salary=data.get('salary')
            )
            return JsonResponse({'status': 'success', 'message': 'Employee added successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', "message": "Invalid JSON data"}, status=400)

    def delete(self, request, emp_id):
        try:
            employee = Employees.objects.get(emp_id=emp_id)
            employee.delete()
            return JsonResponse({'status': 'success', 'message': 'Employee deleted successfully'}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)

    def patch(self, request, emp_id):
        try:
            employee = Employees.objects.get(emp_id=emp_id)
            data = json.loads(request.body)

            # Update the salary if provided in the request
            if 'salary' in data:
                employee.salary = data['salary']
                employee.save()
                return JsonResponse({'status': 'success', 'message': 'Salary updated successfully'}, status=200)

            return JsonResponse({'status': 'failed', 'message': 'No fields to update'}, status=400)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', "message": "Invalid JSON data"}, status=400)
