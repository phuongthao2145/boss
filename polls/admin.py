from django.contrib import admin

# Register your models here.
from .models import *
class InfoAdmin(admin.ModelAdmin):
    fields = [('profileID', 'Identity'), ('fname','lname'),('gender','DateOfBirth','phone'),('sendmail','email', 'status','wpdf'),('address','fromDate','toDate'),'attachment']
    list_display = ('profileID', 'Identity','fname','lname','gender','DateOfBirth','sendmail','email', 'status','wpdf','address','fromDate','toDate','attachment','phone')
    readonly_fields = ['profileID', 'Identity','attachment']

admin.site.register(Info, InfoAdmin)
