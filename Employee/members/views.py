from django.views import View
from .models import Employee
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):

    def get(self, request, emp_id=None, department=None):
        employee_model_list = []
        try:
            if emp_id:
                employee_model_list = Employee.objects.filter(emp_id=emp_id)
            elif department:
                employee_model_list = Employee.objects.filter(department=department)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', "employees": None}, status=400)
        
        employees = []
        for employee in employee_model_list:
            data = {
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "address": employee.address,
                "emp_id": employee.emp_id,
                "mobile": employee.mobile,
                "department": employee.department,
                "salary": str(employee.salary)  # Convert salary to string to avoid serialization issues
            }
            employees.append(data)
        return JsonResponse({'status': 'success', "employees": employees}, status=200)

    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or not request.POST.get('emp_id') or not request.POST.get('mobile') or not request.POST.get('salary'):
            return JsonResponse({'status': 'failed', "message": "All fields are required"}, status=400)

        Employee.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            emp_id=request.POST.get('emp_id'),
            mobile=request.POST.get('mobile'),
            department=request.POST.get('department'),
            salary=request.POST.get('salary')
        )
        return JsonResponse({'status': 'success'}, status=201)

    def put(self, request, emp_id=None):
        if not emp_id:
            return JsonResponse({'status': 'failed', "message": "Employee ID is required"}, status=400)

        try:
            employee = Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', "message": "Employee not found"}, status=404)

        data = json.loads(request.body)
        employee.first_name = data.get('first_name', employee.first_name)
        employee.last_name = data.get('last_name', employee.last_name)
        employee.address = data.get('address', employee.address)
        employee.mobile = data.get('mobile', employee.mobile)
        employee.department = data.get('department', employee.department)
        employee.salary = data.get('salary', employee.salary)
        employee.save()

        return JsonResponse({'status': 'success', "message": "Employee updated successfully"}, status=200)

    def delete(self, request, emp_id=None):
        if not emp_id:
            return JsonResponse({'status': 'failed', "message": "Employee ID is required"}, status=400)

        try:
            employee = Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', "message": "Employee not found"}, status=404)

        employee.delete()

        return JsonResponse({'status': 'success', "message": "Employee deleted successfully"}, status=200)
