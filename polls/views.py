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
from django.utils import timezone

reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + '/polls/lib/reportlabs/fonts')
#https://stackoverflow.com/questions/4899885/how-to-set-any-font-in-reportlab-canvas-in-python
pdfmetrics.registerFont(TTFont('TNR', 'font-times-new-roman (chuan).ttf'))
pdfmetrics.registerFont(TTFont('TNR-B', 'times new roman bold.ttf'))
currentDay = str(datetime.now().day)
currentMonth = str(datetime.now().month)
currentYear = str(datetime.now().year)
absolutepath = os.path.dirname(os.path.dirname(__file__))

@login_required
def changeform(request,id):
    text="Cập nhật thành công"
    type = Type.objects.filter(id=id)
    if request.method == 'POST':
        form = ChangeFormForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']        
            type.update(formName=f.name)
            with open('uploads/' + f.name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            return render(request, 'boss/changeform.html', {'form': form,'id':id,'text':text})
    else:
        form = ChangeFormForm()
    attachment = type.first().formName
    return render(request, 'boss/changeform.html', {'form': form,'id':id,'attachment':attachment})
def changeform1(request):
    return changeform(request,1)
def changeform2(request):
    return changeform(request,2)
#https://www.pdffiller.com/en/functionality/coordinate-pdf.htm
#https://stackoverflow.com/questions/1180115/add-text-to-existing-pdf-using-python
def createpdf():
    infos = Info.objects.order_by('id').reverse()[:10]
    for info in infos:
        if info.formType_id == 1:
             #info student
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("TNR", 12)
            name = u"%s" % info.fname + " " +"%s" % info.lname
            can.drawString(113, 640, name)
            #set address
            addr = info.address
            #https://www.tutorialspoint.com/python-text-wrapping-and-filling
            #20 is line width
            wraped_text = u"\n".join(textwrap.wrap(addr,40))
            t_message = can.beginText()
            t_message.setTextOrigin(113,621)
            t_message.textLines(wraped_text.encode('utf8'))
            can.drawText(t_message)
            #set date of birth
            dateOfBirth =info.DateOfBirth
            can.drawString(411, 640, dateOfBirth)
            #set gender
            gender = "Nữ" if(info.gender == 1) else "Nam"
            can.drawString(383, 621, gender)
            #set p_object
            #p_object = '2'
            #can.drawString(453, 601, p_object)
            #set p_area
            #p_area = '2'
            #can.drawString(442, 581, p_area)
            #set major
            major = info.major
            can.drawCentredString(300, 505, major)
            #set from
            from_d = info.fromDate
            can.drawString(208, 464, from_d)
            #set to
            to_d = info.toDate
            can.drawString(320, 464, to_d)
            #set day
            #can.drawString(380, 221, currentDay)
            #set month
            #can.drawString(472, 221, currentMonth)
        else:
            #info student
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("TNR", 12)
            #set name
            name = u"%s" % info.fname + " " +"%s" % info.lname
            can.drawString(140, 644, name)
            #set address
            addr = info.address
            #https://www.tutorialspoint.com/python-text-wrapping-and-filling
            #20 is line width
            wraped_text = u"\n".join(textwrap.wrap(addr,35))
            t_message = can.beginText()
            t_message.setTextOrigin(139,627)
            t_message.textLines(wraped_text.encode('utf8'))
            can.drawText(t_message)
            #set date of birth
            dateOfBirth =info.DateOfBirth
            can.drawString(411, 644, dateOfBirth)
            #set gender
            gender = "Nữ" if(info.gender == 1) else "Nam"
            can.drawString(383, 627, gender)
            #set major
            major = info.major
            can.drawCentredString(300, 505, major)
            #set from
            #from_d = info.fromDate
            #can.drawString(100, 303, from_d)
            #set to
            #to_d = info.toDate
            #can.drawString(210,303, to_d)
            #save
        can.showPage()
        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)
        #create file
        # read your existing PDF
        formName = Type.objects.filter(id=info.formType_id).first().formName
        filename=os.path.join(absolutepath,'uploads/'+formName)
        existing_pdf = PdfFileReader(open(filename, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        output.addPage(existing_pdf.getPage(1))
        output.addPage(existing_pdf.getPage(2))
        #output.addPage(new_pdf.getPage(0))
        # finally, write "output" to a real file
        outputFile = os.path.join(absolutepath,"uploads/"+ info.attachment)
        outputStream = open(outputFile , "wb")
        try:
            output.write(outputStream)
            outputStream.close()
            Info.objects.filter(Identity=info.Identity).update(wpdf = 1,updated_at=datetime.now())
        except:
            HttpResponse('create PDF error')
def updateSend(self):
    info = Info.objects.filter(sendmail=0).update(sendmail = 1,updated_at=datetime.now())
    return HttpResponseRedirect(reverse('boss:index')) 

def sendmail():
    info = Info.objects.filter(wpdf=1,status=0,sendmail=1).order_by('id').reverse()[:1]
    for to in info:
        type = Type.objects.filter(id=to.formType_id).first()
        subject = "Trường Cao Đẳng Công Nghệ Thủ Đức - "+type.fullName+" Cao đẳng đợt "+str(to.period)+" năm " + currentYear
        body = "Căn cứ kết quả xét tuyển của Hội đồng tuyển sinh đợt "+str(to.period)+" năm "+currentYear+", Chủ tịch Hội đồng tuyển sinh Trường Cao đẳng Công nghệ Thủ Đức trân trọng thông báo Anh/Chị đã trúng tuyển trình độ Cao đẳng chính quy năm "+currentYear+" (đính kèm "+type.fullName+"). Xin chúc mừng Anh/Chị"
        email = to.email
        from_email = None
        msg = EmailMessage(subject, body, from_email, [email])
        filename=os.path.join(absolutepath,'uploads/'+to.attachment)
        msg.attach_file(filename)
        #createpdf
        outputFile = "uploads/"+ to.attachment
        try:
            #send mail
            msg.send()
            Info.objects.filter(Identity=to.Identity).update(status=1,updated_at=datetime.now())
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
    info = Info.objects.all().order_by('status')
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
    #try:
    saveDB(sheet)
    #except:
        #return HttpResponse('save db unsuccess')
    return HttpResponseRedirect(reverse('boss:index'))

#https://stackoverflow.com/questions/31359150/convert-date-from-excel-in-number-format-to-date-format-python
def checkDate(myDate):
    if(isinstance(myDate,float)):
        myDate = datetime(*xlrd.xldate_as_tuple(myDate, 0)).strftime('%d/%m/%Y')
    elif(isinstance(myDate,str)):
        myDate = datetime.strptime(myDate, "%d/%m/%Y").strftime("%d/%m/%Y")
    return myDate

def saveDB(sheet):
    count = 0
    for col in sheet:
        if(count == 0):
            count += 1
            continue    
        prefix = "GBNH" if col[13].value == 1 else "TBTT"
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
            attachment =  prefix+"-"+col[7].value + ".pdf",
            formType_id = col[13].value,
            period = col[14].value
            )
        try:
            info.save()
        except:
            return HttpResponse('save db fail!')
        
#sendmail()
def student(request):
    if(request.method == 'GET'):
        info = Info.objects.filter(phone=request.GET.get('keyword'),wpdf=1).first()
        return render(request,'boss/student.html',{'info':info})
    return render(request, 'boss/student.html')