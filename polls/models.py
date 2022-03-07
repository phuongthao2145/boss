from django.db import models

# Create your models here.
class Info(models.Model):
    mssv = models.CharField(max_length=200)
    attachment = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)



