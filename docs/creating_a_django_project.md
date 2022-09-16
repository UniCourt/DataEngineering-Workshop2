# Creating a Django project

## Installing Django
Django can be installed using pip. Open your terminal and create a folder where you would like to create your Django project. Then run the below commands once you get inside that folder

```buildoutcfg
python -m pip install Django
```
<br />

### Check your Django version

```buildoutcfg
django-admin --version
```

If you are able to see the version it's clear that Django is installed in your system.

### Creating the first Django project
- Select a suitable name for your project. For eg: myworld
- Run the below command to create the first project

```buildoutcfg
django-admin startproject myworld
```

Django creates a myworld folder inside the current folder, with this content:
    
    myworld
        manage.py
        myworld/
            __init__.py
            asgi.py
            settings.py
            urls.py
            wsgi.py
- You can get inside the project folder and run ls command to list down the files and folders inside the project created.

### Run the Django Project
- Once the project is created we can run the project and check if they are created properly.
- Run the below command inside the project folder 
```buildoutcfg
python manage.py runserver
```
- This will produce this result:
  
        Watching for file changes with StatReloader
        Performing system checks...

        System check identified no issues (0 silenced).

        You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
        Run 'python manage.py migrate' to apply them.
        December 02, 2021 - 13:14:51
        Django version 3.2.9, using settings 'myworld.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CTRL-BREAK.
- Now copy the link mentioned in the above log ie., http://127.0.0.1:8000/ and open it in your browser. This should open the sample webpage.
- You can enter CNTRL + C to stop the server and continue with the development. 
- Or you can keep the server running and open a new tab to continue with the rest of the project development.

## Django Create App

### What is an App ?

- An app is a web application that has a specific meaning in your project, like a home page, a contact form.
- We will create a simple Django app that displays 'Hello World'.

#### Create App
- Let the name of the App be Members.
- Go the project folder and run the below command.
```buildoutcfg
python manage.py startapp members
```
- This will create an App called memebrs inside the project folder.
- Now the project folder will look like this

      myworld
        manage.py
        myworld/
        members/
            migrations/
                __init__.py
            __init__.py
            admin.py
            apps.py
            models.py
            tests.py
            views.py
<br />

Now we will modify the required files inside this project and build our project. Let us start with Views.

# Views

- Django views are Python functions that takes http requests and returns http response, like HTML documents.
- Views are usually put in a file called views.py located on your app's folder.
- The views.py file inside the App members will right now look like this:

      from django.shortcuts import render
      
      # Create your views here.

- Go to the members folder and open the views.py using any editor. You can run any of the below command and open the views.py file to edit.
    
      vi views.py  
          or  
      gedit views.py
- Once opened, copy the below content to the views.py file which will help us print "Hello World" in our webpage.
```buildoutcfg
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world!")
```

- Now the views are ready. But how do we call this views? For that we need URL.

# URLs

- Create a file named urls.py in the same folder as the views.py file, and type this code in it:
```buildoutcfg
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

- The urls.py file you just created is specific for the members application.
- We have to do some routing in the root directory myworld as well
- For that go to the myworld folder inside the main project folder myfolder and open the urls.py file
- Then add the include module in the import statement, and also add a path() function in the urlpatterns[] list, with arguments that will route users that comes in via 127.0.0.1:8000/members/.
- Your file should look like this

    
      from django.contrib import admin
      from django.urls import include, path
      
      urlpatterns = [
          path('members/', include('members.urls')),
          path('admin/', admin.site.urls),
      ]
- If your server is not running, go to the main project folder and run the below command to run the server.

      python manage.py runserver
- Once the server start running open the browser and type 127.0.0.1:8000/members/ in the address bar (Previously we were running just 127.0.0.1:8000/, now we added the app members to it, which loaded our views).

# Templates

- Templates has the HTML file which will include the basic structure of the webpage.
- These files should be added in a folder called templates and with file extension .html.
- Now we will create a folder called templates inside the folder members and will add a html file names myfirst.html

  
Go to the folder members. Run the below commands.
      
      mkdir templates
      vi myfirst.html

Add the below content in the file
```buildoutcfg
<!DOCTYPE html>
<html>
<body>

<h1>Hello World!</h1>
<p>Welcome to my first Django project!</p>

</body>
</html>
```

The file structure should be something like this:
    
    myworld
    manage.py
    myworld/
    members/
        templates/
            myfirst.html

## Modify the view file

- Once the template is created, we need to include the template in our view file so that the designed HTML will come up in our web page

Open the views.py file inside the members folder and replace the index view with this:
```buildoutcfg
from django.http import HttpResponse
from django.template import loader

def index(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())
```
- Here we included the template we created inside our view.

## Change Settings
- Now we have to tell Django that a new app is created.
- This is done in the settings.py file in the myworld folder.
- Look for INSTALLED_APPS[] list and add the members app like this:

```buildoutcfg
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members.apps.MembersConfig'
]
```

- Now run the below command in the same folder where manage.py file is present.
```buildoutcfg
python manage.py migrate
```

- This should produce an output like this:
```buildoutcfg
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

(myproject)C:\Users\Your Name\myproject\myworld>
```

- Now start the server again if it is not running by going to the /myworld folder and execute this command:
```buildoutcfg
python manage.py runserver
```

Refresh the browser and now you should be able to see the template content in your webpage.
      
# Models

- A Django model is a table in your database.
- When we created the Django project, we got an empty SQLite database. It was created in the myworld root folder.
- To learn models we will use that database for now.

## Creating a Table/Model
- To create a new table, we must create a new model.
- Open the models.py file in the members folder. By default it will have just a import statement and a comment.
- To add a Members table in our database, start by creating a Members class, and describe the table fields in it:
- Add the below lines of code in models.py file.
```buildoutcfg
from django.db import models

class Members(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
```

- The first field, "firstname" is a Text field, and will contain the first name of the members.
- The second field, "lastname" is also a Text field, with the members' last name.
- Both "firstname" and "lastname" is set up to have a maximum of 255 characters.

In order to create database and tables out of this model we need to do the following steps.

1. Navigate to myworld folder where manage.py file is present and run the below command.
```buildoutcfg
python manage.py makemigrations members
```
This will result in following output.
      
    Migrations for 'members':
    members\migrations\0001_initial.py
      - Create model Members
- Django creates a file with any new changes and stores the file in the /migrations/ folder inside the members folder.
- Now run the below command, in the folder where manage.py is present, to run the migration and create the tables out of the model.
```buildoutcfg
python manage.py migrate
```
This will result in following output:

    Operations to perform:
      Apply all migrations: admin, auth, contenttypes, members, sessions
    Running migrations:
      Applying members.0001_initial... OK

Now the Members table would have created in your database.

# Django Admin Site

- Now that we have added the tables to our database, how do we see that table and perform the CRUD operation to it?
- In order to do that we can use the build admin-site functionality provided by Django to the developers.
- Following steps need to followed :

1. Open the admin.py file in the members folder and add the below lines of code
```buildoutcfg
from django.contrib import admin
from .models import Members

class PersonAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')

admin.site.register(Members,PersonAdmin)
# Register your models here.
```
This will register our models to the admin-site.

2. Create a user that's able to access this dashboard and use it. Run the below command in the folder where manage.py file is present to create the superuser.
```buildoutcfg
python manage.py createsuperuser
```
- This will prompt us to enter username, email address and password. You can add your own username and password. email address can be left blank
- If the user is created it will show the below output.

      Username (leave blank to use 'xxx'): admin
      Email address:
      Password:
      Password (again):
      Superuser created successfully.
3. Now start the server again if it is not running by going to the /myworld folder and execute this command:
```buildoutcfg
python manage.py runserver
```
4. Type http://127.0.0.1:8000/admin/ in your web browser. Now you will be able to see a login page. Add your credentials and login. This will show you the database. 
Currently it is empty. You may use the options present in the admin-site to perform the CRUD operation