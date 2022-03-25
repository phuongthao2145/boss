from dataclasses import field
from django.contrib import admin

# Register your models here.
from .models import *
class InfoAdmin(admin.ModelAdmin):
    fields = [('profileID', 'Identity'), ('fname','lname'),('gender','DateOfBirth','phone','email'),('sendmail','status','wpdf'),('address','period','fromDate','toDate'),('attachment','formType'),('created_at','updated_at')]
    list_display = ('profileID', 'Identity', 'fname','lname','gender','DateOfBirth','phone','sendmail','email', 'status','wpdf','address','period','fromDate','toDate','attachment','formType','created_at','updated_at')
    readonly_fields = ['created_at','updated_at','sendmail','status','wpdf']

class TypeAdmin(admin.ModelAdmin):
    fields = ['typeName','formName','fullName']
    list_display = ('id','typeName','formName','fullName','created_at','updated_at')
    readonly_fields = ['created_at','updated_at']
    
admin.site.register(Info, InfoAdmin)
admin.site.register(Type, TypeAdmin)

