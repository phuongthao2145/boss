from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
