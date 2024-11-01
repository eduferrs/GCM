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
from report.views import home, signin, signup, sair, user_area, create_record, today_records, export_records_csv, export_records_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('sair/', sair, name='sair'),

    path('user_area/', user_area, name='user_area'),
    path('create_record/', create_record, name='create_record'),


    path('today_records/', today_records, name='today_records'),

    path('export/csv/', export_records_csv, name='export_records_csv'),
    path('export/excel/', export_records_excel, name='export_records_excel'),
    
    
]
