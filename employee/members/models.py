from django.db import models

DEPARTMENT_CHOICES = (
    ("OPERATIONS", "OPERATIONS"),
    ("DEVELOPMENT", "DEVELOPMENT"),
    
)

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    emp_id = models.IntegerField()
    mobile = models.CharField(max_length=10)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    salary=models.CharField(max_length=7)

    def __str__(self):
        return self.first_name + " " + self.last_name