#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.views import View
from .models import Emp,  Blog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from . import apps


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
                e_model_list = \
                    Emp.objects.filter(empid=eid)
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
def python_blog_scrap(request):
   apps.start_extraction()
   return JsonResponse({'status': 'sucess', "message" : "Extracted and populated the table."}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class BlogView(View):
    def post(self, request):
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)

        apps.start_extraction(start_date=start_date, end_date=end_date)

        blog_model_list = Blog.objects.filter()

        blogs = []
        for blog in blog_model_list:
            data = {
                "Title": blog.title,
                "Release Date": blog.release_date,
                "Author": blog.author,
                "Blog time": blog.blog_time
            }
            blogs.append(data)

        return JsonResponse({'status': 'success', "students": blogs}, status=200)
