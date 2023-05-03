from django.db import models


DEPT_CHOICES = (
    ("Hiring", "Hiring"),
    ("Training", "Training"),
    ("IT", "IT"),
    ("Accountant", "Accountant"),
)

class Employees(models.Model):
	emp_id = models.IntegerField(default = None)
	name = models.CharField(max_length=200, default = None)
	address = models.CharField(max_length=200,default = None)
	salary = models.IntegerField(default = None)
	dept = models.CharField(max_length=10, choices=DEPT_CHOICES,default = None)

	def __str__(self):
		return self.name
