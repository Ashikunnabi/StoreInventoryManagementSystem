"""StoreInventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from .views import home, input_form, input_form_submit, report, worker_report, worker_report_print

urlpatterns = [
    path('', home, name='home'),
    path('input_form/<catagory>', input_form, name='input_form'),
    path('input_form_submit', input_form_submit, name='input_form_submit'),
    path('report', report, name='report'),
    path('worker_report', worker_report, name='worker_report'),
    path('worker_report/<value>', worker_report, name='worker_report_search'),
    path('worker_report_print', worker_report_print, name='worker_report_print'),
]
