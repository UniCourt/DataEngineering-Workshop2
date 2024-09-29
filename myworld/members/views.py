from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Students

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
                "first_name": student.first_name,
                "last_name": student.last_name,
                "address": student.address,
                "roll_number": student.roll_number,
                "mobile": student.mobile,
                "branch": student.branch
            }
            students.append(data)
        return JsonResponse({'status': 'success', "students": students}, status=200)

    def post(self, request):
        if not request.POST.get('first_name') or not request.POST.get('last_name') or not request.POST.get('address') or not request.POST.get('roll_number') or not request.POST.get('mobile'):
            return JsonResponse({'status': 'failed', "message": "all fields required"}, status=500)

        Students.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            address=request.POST.get('address'),
            roll_number=request.POST.get('roll_number'),
            mobile=request.POST.get('mobile'),
            branch=request.POST.get('branch')
        )
        return JsonResponse({'status': 'success'}, status=200)

    def delete(self, request, rolno=None):
        if not rolno:
            return JsonResponse({'status': 'failed', 'message': 'roll_number required'}, status=400)

        try:
            student = Students.objects.get(roll_number=rolno)
            student.delete()
            return JsonResponse({'status': 'success', 'message': f'Student with roll number {rolno} deleted successfully'}, status=200)
        except Students.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Student not found'}, status=404)
