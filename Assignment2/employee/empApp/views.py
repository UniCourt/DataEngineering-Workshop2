from django.shortcuts import render
from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
            return JsonResponse({'status': 'Failure', "employees": None}, status=400)
        employees = []
        for employee in employee_model_list:
            data = {
                "first_name" : employee.first_name,
                "last_name": employee.last_name,
                "address": employee.address,
                "emp_id": employee.emp_id,
                "phone": employee.phone,
                "salary": employee.salary,
                "dept": employee.dept
            }
            employees.append(data)
        return JsonResponse({'status': 'Success', "employees": employees}, status=200)

    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or  not request.POST.get('emp_id') or not request.POST.get('phone') or not request.POST.get('salary') or not request.POST.get('dept'):
            return JsonResponse({'status': 'Failure', "message" : "Please Enter All the Fields"}, status=400)
 
        Employees.objects.create(
            first_name= request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            address= request.POST.get('address'),
            emp_id= request.POST.get('emp_id'),
            phone= request.POST.get('phone'),
            salary= request.POST.get('salary'),
            dept= request.POST.get('dept'))
        return JsonResponse({'status': 'sucess'}, status=200)
        
    def delete (self, request, emp_id=None):
    	try:
    		obj = Employees.objects.get(emp_id=emp_id)
    		obj.delete()
    		return JsonResponse({'status': 'Success', "message" : "Data Deleted"}, status=200) 
    	except Employees.DoesNotExist:
    		return JsonResponse({'status': 'Failure', "message" : "Employee ID Not Found"}, status=400) 
