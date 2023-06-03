from django.db import models

BRANCH_CHOICES = (
    ("SALES", "SALES"),
    ("AI", "AI"),
    ("ML", "ML"),
    ("CS", "CS"),
)

# Create your models here.
class Emp(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    empid = models.IntegerField()
    salary = models.IntegerField()
    mobile = models.CharField(max_length=10)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)

    def __str__(self):
        return self.first_name + " " + self.last_name
class Blog(models.Model):
    title = models.CharField(max_length=500)
    release_date = models.DateTimeField('Realse Date')
    blog_time = models.CharField(max_length=50)
    author = models.CharField(max_length=200)
    created_date = models.DateTimeField('Created Date', auto_now_add=True, null=True)
    content = models.CharField(max_length=20000)
    recommended =models.CharField(max_length=500)
    path= models.CharField(max_length=500)


   
    def __str__(self):                               
        return self.title
