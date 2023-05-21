from django.db import models

class Members(models.Model):
  EmployeeId = models.CharField(max_length=255)
  Employeename = models.CharField(max_length=255)
  Salary=models.IntegerField()
  companyname = models.CharField(max_length=255)
