from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):

    def get(self, request, emp_id=None, dept=None):
        employee_model_list = []
        try:
            if emp_id:
                employee_model_list = Employees.objects.filter(emp_id=emp_id)
            elif dept:
                employee_model_list = Employees.objects.filter(dept=dept)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "message": "Employee NOT FOUND! Enter a valid employee id"}, status=400)
        employees = []
        for employee in employee_model_list:
            data = {
                "first_name" : employee.first_name,
                "last_name": employee.last_name,
                "emp_id": employee.emp_id,
                "address": employee.address,
                "mobile": employee.mobile,
                "salary": employee.salary,
                "dept": employee.dept
            }
            employees .append(data)
        return JsonResponse({'status': 'success', "employees": employees}, status=200)

    def post(self, request):
            if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or  not request.POST.get('emp_id') or not request.POST.get('mobile') or not request.POST.get('dept') or not request.POST.get('salary'):
                return JsonResponse({'status': 'failed', "message" : "All Fields Required"}, status=500)
            Employees.objects.create(
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                emp_id = request.POST.get('emp_id'),
                address = request.POST.get('address'),
                mobile = request.POST.get('mobile'),
                dept = request.POST.get('dept'),
                salary = request.POST.get('salary'))
            return JsonResponse({'status': 'success', "message" : "Successfully Added"}, status=200)

    def delete (self, request, emp_id=None):
    	    try:
    		    val = Employees.objects.get(emp_id=emp_id)
    		    val.delete()
    		    return JsonResponse({'status': 'success', "message" : "Successfully Deleted"}, status=200) 
    	    except Employees.DoesNotExist:
    		    return JsonResponse({'status': 'failed', "message" : "Employee NOT FOUND!"}, status=400)
    
    def put(self, request, emp_id=None):
		    try:
		        e = Employees.objects.get(emp_id=emp_id)
		    except Employees.DoesNotExist:
		        return JsonResponse({'status': 'failed', "message": "Employee NOT FOUND!"}, status=400)

		    try:
		        data = json.loads(request.body)
		    except json.JSONDecodeError:
		        return JsonResponse({'status': 'failed', "message": "INVALID JSON payload"}, status=400)

		    sal = data.get('salary')
		    if sal is not None:
		        e.salary = sal
		        e.save()
		        return JsonResponse({'status': 'success', "message": "Salary field Updated"}, status=200)
		    else:
		        return JsonResponse({'status': 'failed', "message": "New salary value required"}, status=400)
