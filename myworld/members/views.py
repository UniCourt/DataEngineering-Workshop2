from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):

    def get(self, request, emp_id=None, department=None):
        employee_model_list = []
        try:
            if emp_id:
                employee_model_list = Employees.objects.filter(employee_id=emp_id)
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
                "employee_id": employee.employee_id,
                "mobile": employee.mobile,
                "salary": employee.salary,
                "department": employee.department
            }
            employees.append(data)
        return JsonResponse({'status': 'success', "employees": employees}, status=200)

    def post(self, request):
        if not request.POST.PUT.DELETE.get('first_name') or not request.POST.PUT.DELETE.get('last_name') or not request.POST.PUT.DELETE.get('address') or  not request.POST.PUT.DELETE.get('employee_id') or not request.POST.PUT.DELETE.get('mobile') or not request.POST.PUT.DELETE.get('salary'):
            return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)

        Employees.objects.create(
            first_name= request.POST.PUT.DELETE.get('first_name'),
            last_name= request.POST.PUT.DELETE.get('last_name'),
            address= request.POST.PUT.DELETE.get('address'),
            employee_id= request.POST.PUT.DELETE.get('employee_id'),
            mobile= request.POST.PUT.DELETE.get('mobile'),
            salary= request.POST.PUT.DELETE.get('salary'),
            department= request.POST.PUT.DELETE.get('department'))
        return JsonResponse({'status': 'sucess'}, status=200)
