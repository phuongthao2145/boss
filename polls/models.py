from django.db import models

# Create your models here.
class Info(models.Model):
    profileID = models.CharField(max_length=200)
    attachment = models.CharField(max_length=200)
    fname = models.CharField(max_length=200,null=True)
    lname = models.CharField(max_length=200,null=True)
    majorID = models.IntegerField(null=True)
    major = models.CharField(max_length=200,null=True)
    gender = models.CharField(max_length=200)
    DateOfBirth =  models.CharField(max_length=200,null=True)
    Identity = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    address = models.EmailField(max_length=200,null=True)
    phone = models.IntegerField(null=True)
    fromDate = models.CharField(max_length=200,null=True)
    toDate =  models.CharField(max_length=200,null=True)
    attachment = models.CharField(max_length=200,null=True)
    status = models.IntegerField(default=0)
    wpdf = models.IntegerField(default=0)
    sendmail = models.IntegerField(default=0)
