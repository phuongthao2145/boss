from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100,label="Nhập số điện thoại")