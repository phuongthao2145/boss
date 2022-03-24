from dataclasses import field
from django.contrib import admin

# Register your models here.
from .models import *
class InfoAdmin(admin.ModelAdmin):
    fields = [('profileID', 'Identity'), ('fname','lname'),('gender','DateOfBirth','phone'),('sendmail','email', 'status','wpdf'),('address','fromDate','toDate'),('attachment','formType')]
    list_display = ('id','formType','profileID', 'Identity','fname','lname','gender','DateOfBirth','sendmail','email', 'status','wpdf','address','fromDate','toDate','attachment','phone')
    readonly_fields = ['profileID', 'Identity','attachment']

class TypeAdmin(admin.ModelAdmin):
    fields = ['typeName','formName']
    list_display = ('id','typeName','formName')
    
admin.site.register(Info, InfoAdmin)
admin.site.register(Type, TypeAdmin)

