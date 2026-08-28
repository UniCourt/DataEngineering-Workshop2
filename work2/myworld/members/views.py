from django.shortcuts import render
from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):
    def get(self, request, empid=None, department=None):
        employee_model_list = []
        try:
            if empid:
                employee_model_list = Employees.objects.filter(emp_id=empid)
            elif department:
                employee_model_list = Employees.objects.filter(department=department)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "employees": None}, status=400)
        employees = []
        for employee in employee_model_list:
            data = {
                    "first_name" : employee.first_name,
                    "last_name": employee.last_name,
                    "address": employee.address,
                    "emp_id": employee.emp_id,
                    "salary": employee.salary,
                    "department": employee.department
                }
            employees.append(data)
            return JsonResponse({'status': 'success', "employees": employees}, status=200)
    
    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or  not request.POST.get('emp_id') or not request.POST.get('salary'):
            return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)
        Employees.objects.create(first_name= request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            address= request.POST.get('address'),
            emp_id= request.POST.get('emp_id'),
            salary= request.POST.get('salary'),
            department= request.POST.get('department'))
        return JsonResponse({'status': 'sucess'}, status=200)
    def update(self,request,empid=None):
        try:
            employee = Employees.objects.get(emp_id=empid)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "employees": None}, status=400)
        if request.POST.get('salary'):
            employee.salary=request.POST.get('salary');
            employee.save()
            return JsonResponse({'status': 'success', "message" : "updated salary"}, status=200)
        return JsonResponse({'status': 'failed', "message" : "new salary required"}, status=400)
    def delete(self,request,empid=None):
        try:
            ob= Employees.objects.get(emp_id=empid)
            ob.delete()
            return JsonResponse({'status': 'success', "message" : "deleted data"}, status=200)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "message" : "ID not found"}, status=400)
            
            
            
            
            
            
