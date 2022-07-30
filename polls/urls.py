from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.static import serve
app_name = "boss"

from . import views
from .forms import *
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('boss', views.index, name='index'),
    path('changeform2', views.changeform2, name='changeform2'),
    path('uploadfile', views.upload_file, name='uploadfile'),
    path('changeform1', views.changeform1, name='changeform1'),
    re_path(r'^readfile/(?P<filename>.+)$', views.readfile, name='readfile'),
    path('updatesend',views.updateSend,name='updatesend'),
    path('createpdf',views.createpdf,name='createpdf'),
    path('updatewpdf',views.updatewpdf,name='updatewpdf'),
    re_path(r'^viewpdf/(?P<attachment>.+)$', views.pdf_view, name='viewpdf'),
    path('',views.student,name='student')
]
handler404 = "polls.views.page_not_found_view"

