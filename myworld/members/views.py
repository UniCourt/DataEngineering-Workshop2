from django.views import View
from .models import Students, Employee
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
import json


@method_decorator(csrf_exempt, name='dispatch')
class StudentView(View):

    def get(self, request, rolno=None, branch=None):
        student_model_list = []
        try:
            if rolno:
                student_model_list = Students.objects.filter(roll_number=rolno)
            elif branch:
                student_model_list = Students.objects.filter(branch=branch)
            else:
                student_model_list = Students.objects.all()
        except Students.DoesNotExist:
            return JsonResponse({'status': 'failed', "students": None}, status=400)
        # students = []
        # for student in student_model_list:
        #     data = {
        #         "first_name" : student.first_name,
        #         "last_name": student.last_name,
        #         "address": student.address,
        #         "roll_number": student.roll_number,
        #         "mobile": student.mobile,
        #         "branch": student.branch
        #     }
        #     students.append(data)
        return render(request, 'student_list.html', {'students': student_model_list})

    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or  not request.POST.get('roll_number') or not request.POST.get('mobile'):
            return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)

        Students.objects.create(
            first_name= request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            address= request.POST.get('address'),
            roll_number= request.POST.get('roll_number'),
            mobile= request.POST.get('mobile'),
            branch= request.POST.get('branch'))
        return JsonResponse({'status': 'sucess'}, status=200)
    
    
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):
    
    
    def get(self, request, id=None):
        try:
            employee_id = id or request.GET.get('id')
            if not employee_id:
                return JsonResponse({'status': 'failed', 'message': 'Employee ID is required'}, status=400)
            
            employee = Employee.objects.get(id=employee_id)
            employee_data = {
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "address": employee.address,
                "mobile": employee.mobile,
                "salary": employee.salary,
                "department": employee.department
            }
            return JsonResponse({'status': 'sucess', "employee": employee_data}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', "employee": None}, status=400)

        
    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or  not request.POST.get('mobile'):
            return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)

        Employee.objects.create(
            first_name= request.POST.get('first_name'),
            last_name= request.POST.get('last_name'),
            address= request.POST.get('address'),
            mobile= request.POST.get('mobile'),
            salary= request.POST.get('salary'),
            department= request.POST.get('department'))
        return JsonResponse({'status': 'sucess'}, status=200)

    def delete(self, request, id): 
        try:
            employee = Employee.objects.get(id=id) 
            employee.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failed', "employee": None}, status=400)


    def put(self, request, id):
            try:
                employee = Employee.objects.get(id=id)
                data = json.loads(request.body.decode('utf-8'))
                employee.first_name = data.get('first_name', employee.first_name)
                employee.last_name = data.get('last_name', employee.last_name)
                employee.address = data.get('address', employee.address)
                employee.mobile = data.get('mobile', employee.mobile)
                employee.salary = data.get('salary', employee.salary)
                employee.department = data.get('department', employee.department)
                employee.save()
                return JsonResponse({'status': 'success'}, status=200)
            except Employee.DoesNotExist:
                return JsonResponse({'status': 'failed', "employee": None}, status=404)

