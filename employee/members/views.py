import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Employee

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):

    def get(self, request, empid=None, department=None):
        employee_data = []
        try:
            if empid:
                employee_model_list = Employee.objects.filter(emp_id=empid)
            elif department:
                employee_model_list = Employee.objects.filter(department=department)
            else:
                employee_model_list = Employee.objects.all()  
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', "employee": None}, status=400)
        
        for employee in employee_model_list:
            data = {
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "address": employee.address,
                "emp_id": employee.emp_id,
                "mobile": employee.mobile,
                "department": employee.department,
                "salary": employee.salary
            }
            employee_data.append(data)
            
        return JsonResponse({'status': 'success', "employee": employee_data}, status=200)

    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or not request.POST.get('emp_id') or not request.POST.get('mobile'):
            return JsonResponse({'status': 'failed', "message": "all fields required"}, status=500)

        Employee.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            emp_id=request.POST.get('emp_id'),
            mobile=request.POST.get('mobile'),
            department=request.POST.get('department'),
            salary=request.POST.get('salary')
        )
        return JsonResponse({'status': 'success'}, status=200)

    def delete(self, request, empid=None):
        if not empid:
            return JsonResponse({'status': 'failed', 'message': 'emp_id required'}, status=400)

        try:
            employee = Employee.objects.get(emp_id=empid)
            employee.delete()
            return JsonResponse({'status': 'success', 'message': f'Employee with emp_id {empid} deleted successfully'}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)

    def patch(self, request, empid=None):
        if not empid:
            return JsonResponse({'status': 'failed', 'message': 'emp_id required'}, status=400)

        try:
            employee = Employee.objects.get(emp_id=empid)
            body = json.loads(request.body)  
            salary = body.get('salary')  

            if salary is None:
                return JsonResponse({'status': 'failed', 'message': 'salary is required'}, status=400)

            employee.salary = salary
            employee.save()
            return JsonResponse({'status': 'success', 'message': f'Salary for employee with emp_id {empid} updated successfully'}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Invalid JSON data'}, status=400)