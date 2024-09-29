# the employee directory contains the homework

# Django part 
## 1. project -> django-admin startproject employee
## 2. app -> python manage.py startapp members
## 3. modify settings and migrate the changes
## 4.modify models  ,makemigrations and migrate
## 5. modify admin,createsuperuser
## 6. modify view,url

# docker
## 1. create  2 services web service and postgre service

# database(postgresql)
## docker exec -it psql-db sh -> executes the postgre service
## psql -U postrges -> postgre cmd
## CREATE DATABASE emp_db; -> creatign database
# how to perform crud operations
## 1.docker exec -it workshop_web_container sh ->executes the web service 

## 2.inserting into the table -> CMD curl -X POST http://0.0.0.0:8000/members/rest/employee/ -d "first_name=vijeth&last_name=ferna&address=venor&emp_id=2&mobile=915263890&department=devops&salary=1000"

## 3. reading the data -> curl -X GET http://0.0.0.0:8000/members/rest/employee/id/2

## 4. updating the salary of employee -> curl -X PATCH http://0.0.0.0:8000/members/rest/employee/id/1 -H "Content-Type: application/json" -d '{"salary": 75000}'

## 5. deleting operation curl -X DELETE http://0.0.0.0:8000/members/rest/employee/id/1
