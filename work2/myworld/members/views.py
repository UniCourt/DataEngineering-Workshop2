from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import pdb

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):
    def get(self, request, empid=None, department=None):
        pdb.set_trace()
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
                    "roll_number": employee.emp_id,
                    "mobile": employee.salary,
                    "branch": employee.department
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

    
