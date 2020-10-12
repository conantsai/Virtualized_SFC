"""dashboard URL Configuration

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
from django.contrib import admin
from django.conf.urls import include, url

from board.views import *
from fw.views import *
from ids.views import *
from dpi.views import *
from waf.views import *
from SFC.views import *
from LB.views import *
urlpatterns = [
    url('admin/', admin.site.urls),
#dashboard
    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^side/$', side),
    url(r'^introduce/$', introduce),
    url(r'^SF_status/$', SF_status),

#Fire Wall
    url(r'^fwlist/$', fwlist),
    url(r'^fwaddpage/$', fwaddpage),
    url(r'^fwaction/$', fwaction),

#Intrusion Detection System
    url(r'^ids/$', ids),
    url(r'^idsaction/$', idsaction),

#Deep packet inspection
    url(r'^dpi/$', ntopng),

#Web Application Firewall
    url(r'^waf/', modsecurity),
    url(r'^wafaction/$', modsecaction),

#SFC
    url(r'^SFC/', chain),

#Load balance 
    url(r'^LB/', haproxy),
]
