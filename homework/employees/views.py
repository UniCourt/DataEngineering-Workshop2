from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class EmployeesView(View):
    def get(self, request, eid=None, branch=None):
        employee_model_list = []
        print(isinstance(eid, int))
        try:
            if eid:
                employee_model_list = Employees.objects.filter(emp_id=eid)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "employees": None}, status=400)
        employees = []
        for employee in employee_model_list:
            data = {
                "name" : employee.name,
                "address": employee.address,
                "emp_id": employee.emp_id,
                "mobile": employee.mobile,
                "department": employee.department
            }
            employees.append(data)
        return JsonResponse({'status': 'success', "employees": employees}, status=200)

    def post(self, request):
        if not request.POST.get('name') or not request.POST.get('address') or not request.POST.get('emp_id') or not request.POST.get('mobile') or not request.POST.get('department'):
            return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)

        Employees.objects.create(
            name= request.POST.get('name'),
            address= request.POST.get('address'),
            emp_id= request.POST.get('emp_id'),
            mobile= request.POST.get('mobile'),
            department= request.POST.get('department')
        )
        return JsonResponse({'status': 'sucess'}, status=200)
