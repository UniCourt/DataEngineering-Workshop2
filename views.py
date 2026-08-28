#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.views import View
import json
from .models import Emp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(View):

    def get(
        self,
        request,
        eid=None,
        branch=None,
        ):
        e_model_list = []
        try:
            if eid:
                e_model_list=Emp.objects.filter(empid=eid)
            elif branch:
                e_model_list = \
                    Emp.objects.filter(branch=branch)
        except Emp.DoesNotExist:
            return JsonResponse({'status': 'failed', 'es': None},
                                status=400)
        es = []
        for e in e_model_list:
            data = {
                'first_name': e.first_name,
                'last_name': e.last_name,
                'address': e.address,
                'empid': e.empid,
                'salary' :e.salary,
                'mobile': e.mobile,
                'branch': e.branch,
                }
            es.append(data)
        return JsonResponse({'status': 'success',
                  'students': es}, status=200)

    def post(self, request):
        if not request.POST.get('first_name') \
            or not request.POST.get('last_name') \
            or not request.POST.get('address') \
            or not request.POST.get('empid') \
            or not request.POST.get('salary') \
            or not request.POST.get('mobile'):
            return JsonResponse({'status': 'failed',
                                'message': 'all fields required'},
                                status=500)

        Emp.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            empid=request.POST.get('empid'),
            salary=request.POST.get('salary'),
            mobile=request.POST.get('mobile'),
            branch=request.POST.get('branch'),
            
            )
            return JsonResponse({'status': 'sucess'}, status=200)
        
            
    def delete (self, request, emp_id=None):
    	try:
            val = Employee.objects.get(emp_id=emp_id)
            val.delete()
            return JsonResponse({'status': 'Success', "message" : "Employee data deleted by employee id"}, status=200) 
    	except Employee.DoesNotExist:
            return JsonResponse({'status': 'Failed', "message" : "Employee not found"}, status=400) 
    def put(self, request, emp_id=None):
        try:
            employee = Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'Failed', 'message': 'Employee not found'}, status=400)

        try:
            request_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid JSON payload'}, status=400)

        salary = request_data.get('salary')
        if salary is not None:
            employee.salary = salary
            employee.save()
            return JsonResponse({'status': 'Success', 'message': 'Employee salary updated'}, status=200)
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Please provide a new salary'}, status=400)

        
