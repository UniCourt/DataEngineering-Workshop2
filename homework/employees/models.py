from django.db import models

# Create your models here.
class Employees(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    emp_id = models.IntegerField()
    mobile = models.CharField(max_length=10)
    department = models.CharField(max_length=60)

    def __str__(self):
        return self.name