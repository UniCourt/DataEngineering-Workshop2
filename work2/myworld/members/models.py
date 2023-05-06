from django.db import models

DEPT_CHOICES = (
    ("HR", "IT"),
    ("Accounts", "Manager"),
    ("President", "Clerk"),
    ("Salesman", "Analyst"),
)

# Create your models here.
class Employees(models.Model):
    first_name = models.CharField(max_length=200,default=None)
    last_name = models.CharField(max_length=200,default=None)
    address = models.CharField(max_length=200,default=None)
    emp_id = models.IntegerField(default=None)
    salary = models.IntegerField(default=None)
    department = models.CharField(max_length=10, choices=DEPT_CHOICES,default=None)

    def __str__(self):
        return self.first_name + " " + self.last_name
