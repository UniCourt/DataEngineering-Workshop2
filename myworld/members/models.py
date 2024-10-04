from django.db import models

BRANCH_CHOICES = (
    ("BA", "BA"),
    ("B.COM", "B.COM"),
    ("MBA", "MBA"),
    ("CA", "CA"),
)

EMP_ROLES=(
("HR","HR"),
("Devloper","Devloper"),
("Team_Lead","TeamLead"),
("Tester","Tester"),
)

# Create your models here.
class Students(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    roll_number = models.IntegerField(primary_key=True)
    mobile = models.CharField(max_length=10)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Employee(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    emp_id = models.IntegerField(primary_key=True)
    salary = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    role = models.CharField(max_length=10, choices=EMP_ROLES)

    def __str__(self):
        return self.first_name + " " + self.last_name
