from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views

app_name = "boss"

from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('boss', views.index, name='index'),
    path('uploadfile', views.upload_file, name='uploadfile'),
    re_path(r'^readfile/(?P<filename>.+)$', views.readfile, name='readfile'),
    path('updatesend',views.updateSend,name='updatesend'),
    path('createpdf',views.createpdf,name='createpdf'),
    re_path(r'^viewpdf/(?P<attachment>.+)$', views.pdf_view, name='viewpdf'),
    path('',views.student,name='student')
]
handler404 = "polls.views.page_not_found_view"

