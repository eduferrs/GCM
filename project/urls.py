"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from report.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('sair/', sair, name='sair'),

    path('user_area/', user_area, name='user_area'),
    path('create_record/', create_record, name='create_record'),
    path('notdispatched/', notdispatched, name='notdispatched'),
    path('notfinished/', notfinished, name='notfinished'),


    path('today_records/', today_records, name='today_records'),
    path('all_records/', all_records, name='all_records'),

    path('export/csv/', export_records_csv, name='export_records_csv'),
    path('export/excel/', export_records_excel, name='export_records_excel'),
    path('export2/csv/', export_today_records_csv, name='export_today_records_csv'),
    path('export2/excel/', export_today_records_excel, name='export_today_records_excel'),
    
    
]
