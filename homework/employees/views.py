from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class EmployeesView(View):

    def get(self, request, eid=None, branch=None):
        employee_model_list = []
        try:
            if eid:
                employee_model_list = Employees.objects.filter(emp_id=eid)
            else:
                employee_model_list = Employees.objects.all()
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "employees": None}, status=400)

        employees = []
        for employee in employee_model_list:
            data = {
                "name": employee.name,
                "address": employee.address,
                "emp_id": employee.emp_id,
                "mobile": employee.mobile,
                "department": employee.department
            }
            employees.append(data)
        return JsonResponse({'status': 'success', "employees": employees}, status=200)

    def post(self, request):
        if not request.POST.get('name') or not request.POST.get('address') or not request.POST.get('emp_id') or not request.POST.get('mobile') or not request.POST.get('department'):
            return JsonResponse({'status': 'failed', "message": "all fields required"}, status=500)

        Employees.objects.create(
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            emp_id=request.POST.get('emp_id'),
            mobile=request.POST.get('mobile'),
            department=request.POST.get('department')
        )
        return JsonResponse({'status': 'success'}, status=200)

    def put(self, request, eid=None):
        if not eid:
            return JsonResponse({'status': 'failed', 'message': 'Employee ID is required for update'}, status=400)

        try:
            employee = Employees.objects.get(emp_id=eid)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)

        data = json.loads(request.body)
        employee.name = data.get('name', employee.name)
        employee.address = data.get('address', employee.address)
        employee.mobile = data.get('mobile', employee.mobile)
        employee.department = data.get('department', employee.department)
        employee.save()

        return JsonResponse({'status': 'success', 'message': 'Employee updated successfully'}, status=200)

    def delete(self, request, eid=None):
        if not eid:
            return JsonResponse({'status': 'failed', 'message': 'Employee ID is required for deletion'}, status=400)

        try:
            employee = Employees.objects.get(emp_id=eid)
        except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Employee not found'}, status=404)

        employee.delete()
        return JsonResponse({'status': 'success', 'message': 'Employee deleted successfully'}, status=200)
