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

from .views import login_user, logout_user, home, input_form, input_form_submit, report, report_daily, report_monthly, buy_new_item, graph

urlpatterns = [
    path('login', login_user, name='login_user'),
    path('logout', logout_user, name='logout_user'),
    path('', home, name='home'),
    path('<catagory>/input_form', input_form, name='input_form'),
    path('<catagory>/input_form_submit', input_form_submit, name='input_form_submit'),
    path('<catagory>/report', report, name='report'),
    path('<catagory>/report_daily', report_daily, name='report_daily'),
    path('<catagory>/report_daily/<value>', report_daily, name='report_daily_search'),
    path('<catagory>/report_monthly', report_monthly, name='report_monthly'),
    path('<catagory>/report_monthly/<value>', report_monthly, name='report_monthly_search'),
    path('buy_new_item', buy_new_item, name='buy_new_item'),
    path('graph', graph, name='graph'),
]
