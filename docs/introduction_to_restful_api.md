# Django REST API

### What is API ?
An **API** is a set of programming code that enables data transmission between one software product and another.

**For example**, suppose you wanted to incorporate a map to your business on your website or display a list of your latest tweets. You can’t directly access Google Maps or Twitter — the code that runs those sites sits on Google and Twitter servers. But those platforms provide APIs that let authorized users retrieve data from their sites.


### What is REST API ?
**Representational State Transfer (REST)** is an architectural style that defines a set of constraints to be used for creating web services. REST API is a way of accessing web services in a simple and flexible way without having any processing.
**Ref :**[Click Here](https://www.geeksforgeeks.org/rest-api-introduction/)


### What is Django Rest Framework? 
**The Django REST Framework (DRF)** is a package built on top of Django to create web APIs. One of the most remarkable features of Django is its Object Relational Mapper (ORM) which facilitates interaction with the database in a Pythonic way.

However, we can not send Python objects over a network, and hence need a mechanism to translate Django models in other formats like JSON, XML, and vice-versa. This sometimes challenging process, also called serialization, is made super easy with the Django REST Framework.

## Getting Started with Django Rest Framework
#### First, we create the model simple model of Students to represent the student details.
- Add below Students model in **_/myworld/members/model.py**_ file
    ```python
    from django.db import models

    BRANCH_CHOICES = (
        ("BA", "BA"),
        ("B.COM", "B.COM"),
        ("MBA", "MBA"),
        ("CA", "CA"),
    )

    # Create your models here.
    class Students(models.Model):
        first_name = models.CharField(max_length=200)
        last_name = models.CharField(max_length=200)
        address = models.CharField(max_length=200)
        roll_number = models.IntegerField()
        mobile = models.CharField(max_length=10)
        branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    
        def __str__(self):
            return self.first_name + " " + self.last_name
    ```
  choices: [Click here](https://www.geeksforgeeks.org/how-to-use-django-field-choices/)  
  
#### We created our model and we will register this model with Django.
- To visible this into the admin panel, we will add the following line in the **_/myworld/members/admin.py**_.
    ```python
    from django.contrib import admin
    from .models import Students
    
    class DjStudentAdmin(admin.ModelAdmin):
        list_display = ("first_name", "last_name", "address", "roll_number", "mobile", "branch")
        list_filter = ("branch",)

    # Register your models here.
    admin.site.register(Students, DjStudentAdmin) 
    ```
#### Our new model is registered. We will need to makemigration to reflect the Student table into the database. 
  - Run the following commands inside **workshop_web_container**.
    - Login to the container
        ```commandline
        docker exec -it workshop_web_container sh
        ```
    - Run make Migration
        ```commandline
        python3 manage.py makemigrations  
        python3 manage.py migrate 
        ```
#### Add entries to Student model
- Open this like [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/) and login to admin site if not.
- Click on **Students** model.
- Click on `ADD STUDENT` on top right corner of the admin page to add new students.
- Fill all tge field and click **save** button 
**Note :** Add atleast 10 student information.


### Create Views
DRF allows us to create both class-based and function-based views for the API. We will create the class-based view.
We will use Django's View class. We can define the get(), post() methods so that we can perform the CRUD operations.
- **as_view()**: as_view() class method which returns a function that can be called when a request arrives for a URL matching the associated pattern.
- class-based views : [Click here](https://docs.djangoproject.com/en/4.1/topics/class-based-views/intro/#using-class-based-views:~:text=would%20be%20limited.-,Using%20class%2Dbased%20views,-%C2%B6) 
- Add below code to **_/myworld/members/views.py**_.
    ```python
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
    ```
    - Here in **post()** method we create new student object and in **get()** method we return studnet information in json formate

#### Setup Endpoints for View
- Add below code in **_/myworld/members/urls.py**_.
    ```python
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('rest/student/<int:rolno>', views.StudentView.as_view()),
        path('rest/student/', views.StudentView.as_view()),
        path('rest/student/<str:branch>', views.StudentView.as_view()),
    ]
    ```
#### Trigger API using curl
**CURL** : CURL, which stands for client URL, is a command line tool that developers use to transfer data to and from a server.
- GET Request to get student information
    - Syntax
        ```commandline
        curl -X GET http://0.0.0.0:8000/members/rest/student/<roll number>
        ```
    - Curl cmd
        ```commandline
        curl -X GET http://0.0.0.0:8000/members/rest/student/1
        curl -X GET http://0.0.0.0:8000/members/rest/student/CA
        ```
    Note : Try with wrong roll number
- POST request to add new student
    - Syntax
        ```commandline
        curl -X POST http://0.0.0.0:8000/members/rest/student/ -d "first_name=<str>&last_name=<str>&address=<str>&roll_number=<int>&mobile=<str>&branch=<str>"
        ```
    - Curl cmd
        ```commandline
         curl -X POST http://0.0.0.0:8000/members/rest/student/ -d "first_name=shamith&last_name=H&address=mk&roll_number=3&mobile=897654354&branch=CA"
        ```
    Note : Please check new student is added after running above command.
