from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader  
from django.views import View
from .models import Employees
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
#from .serializers import EmployeeSerializer


def index(request):
  template = loader.get_template('first.html')
  return HttpResponse(template.render())
  
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):
     def get(self, request, employee_id=None):
          employee_model_list = []
          try:
             if employee_id:
                employee_model_list = Employees.objects.filter(employee_id=employee_id)
        
          except Employees.DoesNotExist:
             return JsonResponse({'status': 'failed', "employees": None}, status=400)
          students = []
          for student in employee_model_list:
               data = {
                   "first_name" : student.first_name,
                   "last_name": student.last_name,
                   "employee_salary": student.employee_salary,
                   "employee_id": student.employee_id,
                   "mobile": student.mobile
                }
               students.append(data)
          if len(students)==0:
              return JsonResponse({'status': 'failed', "employees": None}, status=400)
          else:
              return JsonResponse({'status': 'success', "employees": students}, status=200)

     def post(self, request):
          if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('employee_salary') or  not request.POST.get('employee_id') or not request.POST.get('mobile'):
              return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)

          Employees.objects.create(
              first_name= request.POST.get('first_name'),
              last_name= request.POST.get('last_name'),
              employee_salary= request.POST.get('employee_salary'),
              employee_id= request.POST.get('employee_id'),
              mobile= request.POST.get('mobile'))
          return JsonResponse({'status': 'sucess'}, status=200)
          
     
     def put(self, request):
          
          try:
              data = json.loads(request.body)
              employee_id=data['employee_id']
              emp = Employees.objects.get(employee_id=employee_id)
           
          except Employees.DoesNotExist:
              return JsonResponse({'status': 'failed', "employees": None}, status=400)
          try:
                    data=json.loads(request.body)
          except json.JSONDecodeError:
                    return JsonResponse({'status': 'failed', "message" : "invalid"}, status=400)
              
          salary=data.get('employee_salary')
          if salary is not None:
                    emp.employee_salary=salary
                    emp.save()
                    return JsonResponse({'status': 'sucess',"message":"salary updated"}, status=200)
          
          #try:
          else:
                return JsonResponse({'status': 'failure',"message":"salary needed"}, status=500)
                
     def delete(self,request,employee_id=None):
          try:
            emp=Employees.objects.get(employee_id=employee_id)
            emp.delete()
            return JsonResponse({'status': 'sucess',"message":"Employee data deleted"}, status=200)
          except Employees.DoesNotExist:
            return JsonResponse({'status': 'failed', "employees": None}, status=400)
          
