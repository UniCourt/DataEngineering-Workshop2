from django.db import models

class Members(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  def __str__(self):
       return self.first_name + " " + self.last_name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    blog_time = models.TimeField()
    author = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.title
