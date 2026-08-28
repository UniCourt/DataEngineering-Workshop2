from django.views import View
from .models import Employee
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
                employee_model_list = Employee.objects.filter(emp_id=emp_id)
            elif dept:
                employee_model_list = Employee.objects.filter(dept=dept)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'Failure', "employees": None}, status=400)
        employeess = []
        for employee in employee_model_list:
            data = {
                "first_name" : employee.first_name,
                "last_name": employee.last_name,
                "address": employee.address,
                "emp_id": employee.emp_id,
                "mobile": employee.mobile,
                "salary": employee.salary,
                "dept": employee.dept
            }
            employeess.append(data)
        return JsonResponse({'status': 'Success', "employees": employeess}, status=200)

    def post(self, request):
            if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or  not request.POST.get('emp_id') or not request.POST.get('mobile') or not request.POST.get('dept') or not request.POST.get('salary'):
                return JsonResponse({'status': 'Failure', "message" : "*all the fields are required"}, status=400)
            Employee.objects.create(
                first_name= request.POST.get('first_name'),
                last_name= request.POST.get('last_name'),
                address= request.POST.get('address'),
                emp_id= request.POST.get('emp_id'),
                mobile= request.POST.get('mobile'),
                dept= request.POST.get('dept'),
                salary= request.POST.get('salary'))
            return JsonResponse({'status': 'sucess', "message" : "New employee added by id"}, status=200)

    def delete (self, request, emp_id=None):
    	    try:
    		    val = Employee.objects.get(emp_id=emp_id)
    		    val.delete()
    		    return JsonResponse({'status': 'Success', "message" : "Employee data deleted by id"}, status=200) 
    	    except Employee.DoesNotExist:
    		    return JsonResponse({'status': 'Failure', "message" : "Employee not found"}, status=400) 
    

   
    def put(self, request, emp_id=None):
        try:
            employee = Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'Failure', 'message': 'Employee not found'}, status=400)

        try:
            request_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'Failure', 'message': 'Invalid JSON payload'}, status=400)

        salary = request_data.get('salary')
        if salary is not None:
            employee.salary = salary
            employee.save()
            return JsonResponse({'status': 'Success', 'message': 'Employee salary updated'}, status=200)
        else:
            return JsonResponse({'status': 'Failure', 'message': 'Please provide a new salary'}, status=400)

