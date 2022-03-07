from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.urls import reverse
from polls.models import *
from django.contrib.auth.decorators import permission_required
import os
import openpyxl
from pathlib import Path
from django import forms

mssv = []
name = []
def index(request):
    info = Info.objects.all()
    return render(request, 'boss/index.html',{'info': info})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('readfile/' + request.FILES['file'].name)
    else:
        form = UploadFileForm()
    return render(request, 'boss/upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('uploads/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def readfile(request, filename):
    import xlrd
    file_extension = os.path.splitext(filename)
    if file_extension[1] == '.xlsx':
        xlsx_file = Path('uploads', filename)
        wb_obj = openpyxl.load_workbook(xlsx_file)
        # Read the active sheet:
        sheet = wb_obj.active
    elif file_extension[1] == '.xls':
        xlsx_file = Path('uploads', filename)
        wb = xlrd.open_workbook(xlsx_file)
        sheet = wb.sheet_by_index(0)
    else:
        return HttpResponse(("File not supported!"))
    # create attach file
    
    # import info to DB
    try:
        saveDB(sheet)
    except:
        return HttpResponse('save db unsuccess')

    return HttpResponseRedirect(reverse('boss:index'))
def saveDB(sheet):
    count = 0
    for col in sheet:
        if(count == 0):
            count+=1
            continue
        info = Info(mssv=col[0].value,
            attachment=col[0].value+".pdf",
            name=col[1].value,
            email=col[2].value,      
            )
        info.save()