from django.shortcuts import render
from django.views.decorators import csrf
from django.http import JsonResponse
import os
import subprocess
import requests
import json
import requests
import time


"""
fwip = "192.168.16.9:5000"
idsip = "192.168.40.44:5000"
dpiip = "192.168.40.35:5000"
wafip = "192.168.40.39:5000"
"""
fwip = "172.17.0.201:5000"
idsip = "172.17.0.202:6002"
dpiip = "172.17.0.203:3500"
wafip = "172.17.0.204:7000"

natip = "172.17.0.253:5000"
gwip = "172.17.0.3:5000"

loadbalancerip = ""
def index(request):
    return render(request, 'index.html',{})

def side(request):
    fw = json.loads(fw_status(request))
    ids = json.loads(ids_status(request))
    dpi = json.loads(dpi_status(request))
    waf = json.loads(waf_status(request))
    print ("IDS : ")
    print (ids)
    print ("WAF : ")
    print (waf)
    return render(request, 'side.html',{'fw_status':fw, 'ids_status':ids, 'dpi_status':dpi, 'waf_status':waf})

def introduce(request):
    return render(request, 'introduce.html',{})

def fw_status(request):
    r = {"status":False}
    try :
        r = json.loads(requests.post("http://"+fwip+"/iptables/status", timeout=10).content.decode('utf-8'))
    except :
        r = {"status":False}
    r = json.dumps(r)
    return r

def ids_status(request):
    r = {"status":False}
    try :
        r = json.loads(requests.post("http://"+idsip+"/suricata/status", timeout=10).content.decode('utf-8'))
    except :
        r = {"status":False}
    r = json.dumps(r)
    return r

def dpi_status(request):
    r = {"status":False}
    try :
        r = json.loads(requests.post("http://"+dpiip+"/ntopng/status", timeout=10).content.decode('utf-8'))
    except :
        r = {"status":False}
    r = json.dumps(r)
    print ("RETURN")
    print (r)
    return r

def waf_status(request):
    r = {"status":"Unknow"}
    try :
        r = json.loads(requests.post("http://"+wafip+"/modsec/status", timeout=10).content.decode('utf-8'))
    except :
        r = {"status":"Error"}
    r = json.dumps(r)
    print ("WAF STATUS : ")
    print (r)
    return r

def SF_status(request):
    r = {"fw":"Unknow","ids":"Unknow","dpi":"Unknow","waf":"Unknow"}
    fw = {"status":"Unknow"}
    ids = {"status":"Unknow"}
    dpi = {"status":"Unknow"}
    waf = {"status":"Unknow"}
    try :
        fw = json.loads(requests.post("http://"+fwip+"/iptables/status", timeout=10).content.decode('utf-8'))
    except :
        fw = {"status":"except"}
    try :
        ids = json.loads(requests.post("http://"+idsip+"/suricata/status", timeout=10).content.decode('utf-8'))
    except :
        ids = {"status":"except"}
    try :
        dpi = json.loads(requests.post("http://"+dpiip+"/ntopng/status", timeout=10).content.decode('utf-8'))
    except :
        dpi = {"status":"except"}
    try :
        waf = json.loads(requests.post("http://"+wafip+"/modsec/status", timeout=10).content.decode('utf-8'))
    except :
        waf = {"status":"except"}
    r = {"fw":fw["status"],"ids":ids["status"],"dpi":dpi["status"],"waf":waf["status"]}
    #r = json.dumps(r)
    print ("SF-WAF : ")
    print (waf)
    return JsonResponse(r)
