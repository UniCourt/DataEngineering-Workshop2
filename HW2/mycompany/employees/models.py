from django.db import models

DEPARTMENT_CHOICES = (
    ("HR", "HR"),
    ("Finance","Finance"),
    ("Marketing", "Marketing"),
    ("Sales","Sales"),
    ("Planning", "Planning"),
    ("Security","Security"),
    ("Engineering", "Engineering"),
)

# Create your models here.
class Employees(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	emp_id = models.BigAutoField(primary_key=True)
	address = models.CharField(max_length=200)
	mobile = models.CharField(max_length=10)
	dept = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
	salary = models.IntegerField()
	
	def __str__(self):
		return self.first_name + " " + self.last_name
