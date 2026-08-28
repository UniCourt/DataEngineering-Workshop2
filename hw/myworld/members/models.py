from django.db import models

class Members(models.Model):
  Employeename = models.CharField(max_length=255)
  EmployeeId = models.CharField(max_length=255)
  Salary=models.IntegerField()
