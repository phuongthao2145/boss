from django.contrib import admin

# Register your models here.
from .models import *
class InfoAdmin(admin.ModelAdmin):
    fields = ['id','profileID','sendmail', 'fname','lname','gender','DateOfBirth', 'Identity','email','address','fromDate','toDate', 'status','attachment','wpdf']
    list_display = ('id','profileID','sendmail', 'fname','lname','gender','DateOfBirth', 'Identity','email','address','fromDate','toDate', 'status','attachment','wpdf')
    readonly_fields = ()

admin.site.register(Info, InfoAdmin)
