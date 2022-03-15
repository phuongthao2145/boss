from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views


app_name = "boss"

from . import views

urlpatterns = [
    path('auth/login/', auth_views.LoginView.as_view(template_name='authticate/login.html'), name='login'),
    path('auth/logout', auth_views.LogoutView.as_view(template_name='authticate/logout.html'), name='logout'),
    path('', views.index, name='index'),
    path('uploadfile', views.upload_file, name='uploadfile'),
    re_path(r'^readfile/(?P<filename>.+)$', views.readfile, name='readfile'),
    path('sendmail/<mssv>',views.sendmail,name='sendmail'),
    path('createpdf',views.createpdf,name='createpdf'),
]
