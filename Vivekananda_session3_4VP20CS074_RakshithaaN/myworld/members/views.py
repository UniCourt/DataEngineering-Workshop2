from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.template import loader
from django.views import View
from .models import Students
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Students, Blog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from . import apps

def index(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())
  



@method_decorator(csrf_exempt, name='dispatch')
class BlogView(View):
    def post(self, request):
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        no_of_articles = request.POST.get('no_of_articles', None)
        start_id = request.POST.get('start_id', None)

        apps.start_extraction(start_date=start_date, end_date=end_date, no_of_articles=no_of_articles, start_id=start_id)

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

        return JsonResponse({'status': 'success', "Blogs": blogs}, status=200)




class StudentView(View):

    def get(self, request, rolno=None, branch=None):
         student_model_list = []
         try:
           if rolno:
              student_model_list = Students.objects.filter(roll_number=rolno)
           elif branch:
              student_model_list = Students.objects.filter(branch=branch)
         except Students.DoesNotExist:
              return JsonResponse({'status': 'failed', "students": None}, status=400)
         students = []
         for student in student_model_list:
                data = {
                   "first_name" : student.first_name,
                   "last_name": student.last_name,
                   "address": student.address,
                   "roll_number": student.roll_number,
                   "mobile": student.mobile,
                   "branch": student.branch
                 }
                students.append(data)
         return JsonResponse({'status': 'success', "students": students}, status=200)

    def post(self, request):
           if not request.POST.get('first_name') or not        request.POST.get('last_name') or not request.POST.get('address') or  not   request.POST.get('roll_number') or not request.POST.get('mobile'):
                return JsonResponse({'status': 'failed', "message" : "all fields required"}, status=500)

           Students.objects.create(
                 first_name= request.POST.get('first_name'),
                 last_name= request.POST.get('last_name'),
                 address= request.POST.get('address'),
                 roll_number= request.POST.get('roll_number'),
                 mobile= request.POST.get('mobile'),
                 branch= request.POST.get('branch'))
           return JsonResponse({'status': 'sucess'}, status=200)
           
           
def python_blog_scrap(request):
           apps.start_extraction()
           return JsonResponse({'status': 'sucess', "message" : "Extracted and populated the table."}, status=200)

