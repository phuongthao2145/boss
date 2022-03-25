from django.db import models
from datetime import datetime

# Create your models here.

class Type(models.Model):
    typeName = models.CharField(max_length=200,null=True)
    formName =  models.CharField(max_length=200,null=True)
    created_at=models.DateField(default=datetime.now, blank=True)
    updated_at=models.DateField(default=datetime.now, blank=True)
    def __str__(self):
        return self.typeName   
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
    email = models.EmailField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=20,null=True)
    fromDate = models.CharField(max_length=200,null=True)
    toDate =  models.CharField(max_length=200,null=True)
    attachment = models.CharField(max_length=200,null=True)
    status = models.IntegerField(default=0)
    wpdf = models.IntegerField(default=0)
    sendmail = models.IntegerField(default=0)
    formType = models.ForeignKey('Type', on_delete=models.RESTRICT, null=True, related_name='type', blank=True)
    period = models.IntegerField(default=0)
    created_at=models.DateField(default=datetime.now, blank=True)
    updated_at=models.DateField(default=datetime.now, blank=True)
    def __str__(self):
        return self.profileID



