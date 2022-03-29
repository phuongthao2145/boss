from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Chọn tệp",required=True)
class ChangeFormForm(forms.Form):
    file = forms.FileField(label="Chọn tệp",required=True)