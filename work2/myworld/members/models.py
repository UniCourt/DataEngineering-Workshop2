from django.db import models

DEPT_CHOICES = (
    ("HR", "IT"),
    ("Accounts", "Manager"),
    ("President", "Clerk"),
    ("Salesman", "Analyst"),
)

# Create your models here.
class Employees(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    emp_id = models.IntegerField()
    salary = models.CharField(max_length=10)
    department = models.CharField(max_length=10, choices=DEPT_CHOICES)

    def __str__(self):
        return self.first_name + " " + self.last_name
