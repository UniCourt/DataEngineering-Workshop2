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
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	emp_id = models.BigAutoField(primary_key=True)
	mobile = models.CharField(max_length=10)
	dept =models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
	salary = models.IntegerField()
	
	def __str__(self):
		return self.first_name + " " + self.last_name




