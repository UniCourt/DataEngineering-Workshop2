from django.db import models

class Members(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phoneNum = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

class Blog(models.Model):
    title = models.CharField(max_length=500)
    release_date = models.DateTimeField('Release Date')
    blog_time = models.CharField(max_length=50)
    author = models.CharField(max_length=200)
    created_date = models.DateTimeField('Created Date', auto_now_add=True, null=True)
   
    def __str__(self):                               
        return self.title