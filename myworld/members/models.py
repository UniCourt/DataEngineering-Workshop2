from django.db import models

BRANCH_CHOICES = (
    ("BA", "BA"),
    ("B.COM", "B.COM"),
    ("MBA", "MBA"),
    ("CA", "CA"),
)


# Create your models here.
class Students(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    roll_number = models.IntegerField()
    mobile = models.CharField(max_length=10)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Blog(models.Model):
    title = models.CharField(max_length=500)
    release_date = models.DateField('Release Date', null=True, blank=True)
    blog_time = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    total_comments = models.IntegerField(default=0)
    recommended_google = models.IntegerField(default=0)
    html_file_path = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField('Created Date', auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class Employee(models.Model):
    emp_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.emp_id} - {self.first_name} {self.last_name}"