from django.shortcuts import render
from board.views import wafip
import requests
import json

def modsecurity(request):
    rns = {"status":"Unknow"}
    rms = {"status":"Unknow"}
    try:
        rns = json.loads(requests.post("http://"+wafip+"/modsec/nginx-status", timeout=10).content.decode('utf-8'))
    except Exception as e:
        rns = {"status":False}
    try:
        rms = json.loads(requests.post("http://"+wafip+"/modsec/nginx-modsec", timeout=10).content.decode('utf-8'))
    except Exception as e:
        rms = {"status":False}
    rlist = []
    if {"status": True} == rms and {"status": True} == rns :
        try:
            rlist = json.loads(requests.post("http://"+wafip+"/modsec/list", timeout=10).content.decode('utf-8'))
        except Exception as e:
            rlist = []
    return render(request, 'modsecurity.html', {'nginx_status':rns,'mod_status':rms,'modsec_list':rlist})

def modsecaction(request):
    if request.method == "POST":
        if request.POST.get('delete'):
            rlt = "Trying delete rule"
            rns = {"status":"Unknow"}
            rms = {"status":"Unknow"}
            rdr = {"status":"Unknow"}

            result = "WAF"
            successfulCounter = 0
            failedCounter = 0
            otherCounter = 0
            check_box_list = request.POST.getlist('delete_box')
            rule_list = request.POST.getlist('Modrule')
            for index in check_box_list:
                index = int(index)
                index += -1
                rule = rule_list[index]
                post_data = {"rule":rule}
                try :
                    rdr = str(json.loads(requests.post("http://"+wafip+"/modsec/delete",post_data).content.decode('utf-8')))
                    if rdr.find("True"):
                        successfulCounter += 1
                    elif {"status": False} == rdr:
                        failedCounter += 1
                    else:
                        otherCounter += 1
                except Exception as e:
                    pass
            result = str(successfulCounter) + " rule(s) delete successfully, and " + str(failedCounter + otherCounter) + " rule(s) delete failed"

            try:
                rns = json.loads(requests.post("http://"+wafip+"/modsec/nginx-status").content.decode('utf-8'))
                #rns = json.loads(requests.post("http://"+wafip+"/modsec/nginx-status", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rns = {"status":False}
            try:
                rms = json.loads(requests.post("http://"+wafip+"/modsec/nginx-modsec").content.decode('utf-8'))
                #rms = json.loads(requests.post("http://"+wafip+"/modsec/nginx-modsec", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rms = {"status":False}
            """if {'status': True} == rdr:
                rlt = "Delete rule successfully"
            elif {'status': "invaild delete"} == rdr:
                rlt = "Invaild delete, please try again"
            elif {'status': "invaild delete but recovery"} == rdr:
                rlt = "Invaild delete, do nothing"
            elif {'status': "invaild delete and recovery failed"} == rdr:
                rlt = "Invaild delete and recovery failed, please reset your nginx"
            else:
                rlt = "Unknow error, please reset your nginx" """
            rlist = []
            try:
                rlist = json.loads(requests.post("http://"+wafip+"/modsec/list").content.decode('utf-8'))
                #rlist = json.loads(requests.post("http://"+wafip+"/modsec/list", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rlist = []
            return render(request,'modsecurity.html',{'Counter':failedCounter + otherCounter,"nginx_status":rns,'mod_status':rms,"rlt":result,"add_result":result,'modsec_list':rlist})

        if request.POST.get('send'):
            comm = request.POST['CMD']
            post_data = {"comm":comm}
            rlt = "Trying add " + request.POST['CMD'] + " "
            rns = {"status":"Unknow"}
            rms = {"status":"Unknow"}
            rar = {"status":"Unknow"}
            try:
                rar = json.loads(requests.post("http://"+wafip+"/modsec/add-rule",post_data).content.decode('utf-8'))
                #rar = json.loads(requests.post("http://"+wafip+"/modsec/add-rule",post_data, timeout=60).content.decode('utf-8'))
            except Exception as e:
                rar = {"status":False}
            try:
                rns = json.loads(requests.post("http://"+wafip+"/modsec/nginx-status").content.decode('utf-8'))
                #rns = json.loads(requests.post("http://"+wafip+"/modsec/nginx-status", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rns = {"status":False}
            try:
                rms = json.loads(requests.post("http://"+wafip+"/modsec/nginx-modsec").content.decode('utf-8'))
                #rms = json.loads(requests.post("http://"+wafip+"/modsec/nginx-modsec", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rms = {"status":False}
            if {'status': True} == rar:
                rlt = "Add " + request.POST['CMD'] + " successfully"
            elif {'status': "invaild cmd"} == rar:
                rlt = "Invaild command, please check your commad"
            elif {'status': "invaild cmd but recovery"} == rar:
                rlt = "Invaild command, but recovery successfully"
            elif {'status': "invaild cmd and recovery failed"} == rar:
                rlt = "Invaild command and recovery failed, please reset your nginx"
            else:
                rlt = "Unknow error, please reset your nginx"
            rlist = []
            try:
                rlist = json.loads(requests.post("http://"+wafip+"/modsec/list").content.decode('utf-8'))
                #rlist = json.loads(requests.post("http://"+wafip+"/modsec/list", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rlist = []
            return render(request,'modsecurity.html',{"nginx_status":rns,'mod_status':rms,"rlt":rlt,"add_result":rar,'modsec_list':rlist})
        elif request.POST.get('restart'):
            rns = {"status":"Unknow"}
            rms = {"status":"Unknow"}
            rnrs = {"status":"Unknow"}
            try:
                rnrs = json.loads(requests.post("http://"+wafip+"/modsec/nginx-restart").content.decode('utf-8'))
                #rnrs = json.loads(requests.post("http://"+wafip+"/modsec/nginx-restart", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rnrs = {"status":False}
            try:
                rns = json.loads(requests.post("http://"+wafip+"/modsec/nginx-status").content.decode('utf-8'))
                #rns = json.loads(requests.post("http://"+wafip+"/modsec/nginx-status", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rns = {"status":False}
            try:
                rms = json.loads(requests.post("http://"+wafip+"/modsec/nginx-modsec").content.decode('utf-8'))
                #rms = json.loads(requests.post("http://"+wafip+"/modsec/nginx-modsec", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rms = {"status":False}
            R={'status': "Restart Failed"}
            if {'status': True} == rnrs and {'status': True} == rns :
                R={'status': "Restart Successful"}
            rlist = []
            try:
                rlist = json.loads(requests.post("http://"+wafip+"/modsec/list").content.decode('utf-8'))
                #rlist = json.loads(requests.post("http://"+wafip+"/modsec/list", timeout=10).content.decode('utf-8'))
            except Exception as e:
                rlist = []
            return render(request,'modsecurity.html',{"nginx_status":R,'mod_status':rms,'modsec_list':rlist})
