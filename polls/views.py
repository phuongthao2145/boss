#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from django.core.mail import EmailMessage
from django.conf import settings
import io
import PyPDF2
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
def createpdf(identity,outputFile):
    #info student
    info = Info.objects.filter(Identity=identity).first()
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
    # read your existing PDF
    existing_pdf = PdfFileReader(open("uploads/GBNH.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    #output.addPage(new_pdf.getPage(0))
    # finally, write "output" to a real file
    outputStream = open(outputFile , "wb")
    try:
        output.write(outputStream)
        outputStream.close()
    except:
        return HttpResponse('write file fail!!!')
    return HttpResponse('write file succsessfully!!!')

def sendmail(request,identity):
    if(identity == 'all'):
        info = Info.objects.values_list('email', flat=True).distinct().exclude(status=1)
        to = list(info)
        update_status = Info.objects.filter(email = info)
    else:
        try:
            info = Info.objects.filter(Identity=identity).exclude(status=1).first().email
        except:
            return HttpResponse('This email already sent!')
        to = [info]
        update_status = Info.objects.filter(email = info)
    subject = "Giay bao nhap hoc"
    body = "giay bao nhap hoc"
    from_email = None
    msg = EmailMessage(subject, body, from_email, to)
    msg.attach_file('uploads/output.pdf')
    try:
        msg.send()
        update_status.update(status=1)
    except:
        return HttpResponse('Sent mail fail')
    return HttpResponse('Sent mail Successfully')


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
    except ex:
        return HttpResponse('save db unsuccess' + ex)
    #createpdf('052204008562','uploads/052204008562.pdf')
    return HttpResponseRedirect(reverse('boss:index'))

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
            DateOfBirth = datetime.strptime(col[5].value, "%d/%m/%Y").strftime("%d/%m/%Y"),
            profileID = col[6].value,
            Identity = col[7].value,
            phone = col[8].value,
            address = col[9].value,
            email = col[10].value, 
            #https://stackoverflow.com/questions/31359150/convert-date-from-excel-in-number-format-to-date-format-python
            fromDate = datetime(*xlrd.xldate_as_tuple(col[11].value, 0)).strftime('%d/%m/%Y'),
            toDate = datetime(*xlrd.xldate_as_tuple(col[12].value, 0)).strftime('%d/%m/%Y'),
            attachment =  col[7].value + ".pdf"
            )
        try:
            info.save()
        except:
            return HttpResponse(col[11].value)
        #create file
        # Open a file
        op = open("uploads/"+ col[7].value + ".pdf", "wb")
        # Close opened file
        op.close()
        #createpdf
        outputFile = "uploads/"+ col[7].value + ".pdf"
        try:
            createpdf(col[7].value,outputFile)
        except:
            HttpResponse('create PDF error')
