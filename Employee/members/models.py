from django.db import models

DEPARTMENT_CHOICES = (
    ("HR", "Human Resources"),
    ("FIN", "Finance"),
    ("ENG", "Engineering"),
    ("MKT", "Marketing"),
)

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    emp_id = models.IntegerField()
    mobile = models.CharField(max_length=10)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
