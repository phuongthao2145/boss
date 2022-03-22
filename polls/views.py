#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from django.urls import reverse
from polls.models import *
from django.contrib.auth.decorators import login_required
import os
import openpyxl
from pathlib import Path
from django import forms
from django.core.mail import EmailMessage
from django.conf import settings
import io
from django.http import FileResponse
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont 
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
import xlrd
import textwrap
from io import open
from datetime import datetime
from django.conf import settings
reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + '/polls/lib/reportlabs/fonts')
#https://stackoverflow.com/questions/4899885/how-to-set-any-font-in-reportlab-canvas-in-python
pdfmetrics.registerFont(TTFont('TNR', 'times new roman.ttf'))
pdfmetrics.registerFont(TTFont('TNR-B', 'times new roman bold.ttf'))
currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
#https://www.pdffiller.com/en/functionality/coordinate-pdf.htm
#https://stackoverflow.com/questions/1180115/add-text-to-existing-pdf-using-python
@login_required
def createpdf():
    infos = Info.objects.exclude(status=1).order_by('id')[:10]
    for info in infos:
        #info student
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("TNR-B", 12)
        name = "%s" % info.fname + " " +"%s" % info.lname
        can.drawString(110, 639, name)
        #set address
        addr = info.address
        #https://www.tutorialspoint.com/python-text-wrapping-and-filling
        #20 is line width
        wraped_text = u"\n".join(textwrap.wrap(addr,40))
        t_message = can.beginText()
        t_message.setTextOrigin(100,620)
        t_message.textLines(wraped_text)
        can.drawText(t_message)
        #set date of birth
        dateOfBirth =info.DateOfBirth
        can.drawString(411, 639, dateOfBirth)
        #set gender
        gender = "Nữ" if(info.gender == 1) else "Nam"
        can.drawString(383, 620, gender)
        #set p_object
        p_object = '2'
        can.drawString(453, 601, p_object)
        #set p_area
        p_area = '2'
        can.drawString(442, 581, p_area)
        #set major
        major = info.major
        can.drawCentredString(300, 466, major)
        #set from
        from_d = info.fromDate
        can.drawString(215, 426, from_d)
        #set to
        to_d = info.toDate
        can.drawString(346, 426, to_d)
        #set day
        can.drawString(423, 221, str(currentDay))
        #set month
        can.drawString(472, 221, str(currentMonth))
        #set carpentry
        carpentry = "Ký tên"
        can.drawString(400, 150, carpentry)
        #save
        can.showPage()
        can.save()
        print(can.drawText(t_message))
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)
        #create file
        #Open a file
        #op = open("uploads/"+ info.attachment, "wb")
        # read your existing PDF
        existing_pdf = PdfFileReader(open("uploads/GBNH.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        #output.addPage(new_pdf.getPage(0))
        # finally, write "output" to a real file
        outputFile = "uploads/"+ info.attachment
        outputStream = open(outputFile , "wb")
        try:
            output.write(outputStream)
            outputStream.close()
            Info.objects.filter(Identity=info.Identity).update(wpdf = 1)
        except:
            HttpResponse('create PDF error')
@login_required
def updateSend(self):
    info = Info.objects.filter(sendmail  = 0).update(sendmail = 1)
    return HttpResponseRedirect(reverse('boss:index')) 
@login_required
def sendmail():
    info = Info.objects.filter(wpdf=1,status=0,sendmail=1).order_by('id')[:2]
    for to in info:
        email = to.email
        subject = "Giấy Báo Nhập Học"
        body = "Giấy báo nhập học"
        from_email = None
        msg = EmailMessage(subject, body, from_email, [email])
        msg.attach_file('uploads/' + to.attachment)
        #createpdf
        outputFile = "uploads/"+ to.attachment
        try:
            #send mail
            msg.send()
            Info.objects.filter(Identity=to.Identity).update(status = 1)
            to.refresh_from_db()
        except:
            HttpResponse('send mail error')
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
from django.http import FileResponse, Http404
def pdf_view(request,attachment):
    try:
        return FileResponse(open('uploads/'+attachment, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
@login_required
def index(request):
    info = Info.objects.all()
    return render(request, 'boss/index.html',{'info': info})
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('readfile/' + request.FILES['file'].name)
    else:
        form = UploadFileForm()
    return render(request, 'boss/upload.html', {'form': form})

@login_required
def handle_uploaded_file(f):
    with open('uploads/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def readfile(request, filename):
    file_extension = os.path.splitext(filename)
    if file_extension[1] == '.xlsx':
        xlsx_file = Path('uploads', filename)
        wb = openpyxl.load_workbook(xlsx_file)
        # Read the active sheet:
        sheet = wb.active
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

#https://stackoverflow.com/questions/31359150/convert-date-from-excel-in-number-format-to-date-format-python
def checkDate(myDate):
    if(isinstance(myDate,float)):
        myDate = datetime(*xlrd.xldate_as_tuple(myDate, 0)).strftime('%d/%m/%Y')
    elif(isinstance(myDate,str)):
        myDate = datetime.strptime(myDate, "%d/%m/%Y").strftime("%d/%m/%Y")
    return myDate

@login_required
def saveDB(sheet):
    count = 0
    for col in sheet:
        if(count == 0):
            count += 1
            continue
        info = Info(majorID = col[0].value,
            major = col[1].value,
            fname = col[2].value,
            lname = col[3].value,
            gender = col[4].value,
            DateOfBirth = checkDate(col[5].value),
            profileID = col[6].value,
            Identity = col[7].value,
            phone = col[8].value,
            address = col[9].value,
            email = col[10].value, 
            fromDate = checkDate(col[11].value),
            toDate = checkDate(col[12].value),
            attachment =  col[7].value + ".pdf",
            )
        try:
            info.save()
        except:
            return HttpResponse(col[11].value)
        
#sendmail()
       
def student(request):
    if(request.method == 'GET'):
        form = SearchForm()
        if form.is_valid():
            handle_search(request,form.cleaned_data['keyword'])
    return render(request, 'boss/student.html',{'form': form})

def handle_search(request,keyword):
    info = Info.objects.filter(phone='943727475').first()
    return render(request,'boss/student.html',{'info':info})