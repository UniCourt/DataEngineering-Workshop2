from django.db import models

DEPARTMENT_CHOICES = (
    ("HR", "HR"),
    ("Engineering", "Engineering"),
    ("Marketing", "Marketing"),
    ("Planning", "Planning"),
    ("Sales","Sales"),
    ("Finance","Finance"),
    ("Operations","Operations"),
)




class Employee(models.Model):
	first_name = models.CharField(max_length=200, default = None)
	last_name = models.CharField(max_length=200, default = None)
	address = models.CharField(max_length=200,default = None)
	emp_id = models.IntegerField(default = None)
	mobile = models.CharField(max_length=10, default = None)
	dept =models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
	salary = models.IntegerField(default = None)
	
	def __str__(self):
		return self.first_name + " " + self.last_name




