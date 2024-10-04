from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Employee
import json

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            employee = Employee.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                address=data['address'],
                mobile=data['mobile'],
                salary=data['salary']
            )
            return JsonResponse({'status': 'success', 'emp_id': employee.emp_id}, status=201)
        except KeyError:
            return JsonResponse({'status': 'failed', 'message': 'All fields are required'}, status=400)

    def get(self, request, emp_id=None):
        if emp_id:
            try:
                employee = Employee.objects.get(emp_id=emp_id)
                return JsonResponse({
                    'status': 'success',
                    'employee': {
                        'first_name': employee.first_name,
                        'last_name': employee.last_name,
                        'address': employee.address,
                        'mobile': employee.mobile,
                        'salary': str(employee.salary)
                    }
                }, status=200)
            except Employee.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)
        else:
            employees = list(Employee.objects.values())
            return JsonResponse({'status': 'success', 'employees': employees}, status=200)

    def delete(self, request, emp_id):
        try:
            employee = Employee.objects.get(emp_id=emp_id)
            employee.delete()
            return JsonResponse({'status': 'success', 'message': 'Employee deleted'}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)

    def put(self, request, emp_id):
        data = json.loads(request.body)
        try:
            employee = Employee.objects.get(emp_id=emp_id)
            employee.salary = data.get('salary', employee.salary)
            employee.save()
            return JsonResponse({'status': 'success', 'message': 'Salary updated'}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)
