from django.views import View
from .models import Students
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
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
    
