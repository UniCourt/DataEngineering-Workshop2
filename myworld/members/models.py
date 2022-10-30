from django.db import models

class Members(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

DEPARTMENT_CHOICES = (
    ("HR", "HR"),
    ("IT", "IT"),
    ("AI", "AI"),
    ("RD", "RD"),
)

# Create your models here.
class Employees(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    employee_id = models.IntegerField()
    mobile = models.CharField(max_length=10)
    salary = models.IntegerField()
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.first_name + " " + self.last_name
