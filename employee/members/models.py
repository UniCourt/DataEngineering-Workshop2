from django.db import models



# Create your models here.
class Employees(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    employee_salary = models.IntegerField()
    employee_id = models.IntegerField(primary_key=True)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name + " " + self.last_name
