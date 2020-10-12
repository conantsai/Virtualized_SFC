from django.shortcuts import render
import json
import requests
import time
import threading
from board.views import idsip

suricata_status = "Unknow"
suricata_delete_rule = 0

def ids(request):
    global suricata_status
    r = {"status":False}
    try :
        r = json.loads(requests.post("http://"+idsip+"/suricata/status", timeout=2).content.decode('utf-8'))
    except Exception as e:
        r = {"status":False}
    CMDresult = ""
    if {"status": True} == r :
        if suricata_status == "Restarting":
            CMDresult = "Restart successfully"
            suricata_status = ""
        elif suricata_status == "Updating":
            CMDresult = "Update successfully"
            suricata_status = ""
        elif suricata_status == "Adding":
            CMDresult = "Adding rule successfully"
            suricata_status = ""
    rlist = []
    if {'status': True} == r :
        try:
            rlist = json.loads(requests.post("http://"+idsip+"/suricata/list", timeout=2).content.decode('utf-8'))
        except Exception as e:
            rlist = []
    return render(request, 'ids.html',{"rlt":CMDresult,'suricata_list':rlist,})

def idsaction(request):
    r = {"status":False}
    if request.method == "POST":
        if request.POST.get('delete'):
            rdr = {"status":"Unknow"}

            CMDresult = "Unknow"
            successfulCounter = 0
            failedCounter = 0
            otherCounter = 0
            check_box_list = request.POST.getlist('delete_box')
            rule_list = request.POST.getlist('Idsrule')
            for index in check_box_list:
                index = int(index)
                index += -1
                rule = rule_list[index]
                post_data = {"rule":rule}
                try :
                    rdr = str(json.loads(requests.post("http://"+idsip+"/suricata/delete",post_data).content.decode('utf-8')))
                    if rdr.find("True"):
                        successfulCounter += 1
                    elif {"status": False} == rdr:
                        failedCounter += 1
                    else:
                        otherCounter += 1
                    try :
                        rdr = json.loads(requests.post("http://"+idsip+"/suricata/update").content.decode('utf-8'))
                    except Exception as e:
                        rdr = {"status":False}
                except Exception as e:
                    pass
            suricata_delete_rule = successfulCounter
            CMDresult = str(successfulCounter) + " rule(s) delete successfully, and " + str(failedCounter + otherCounter) + " rule(s) delete failed"
            try:
                thread1 = threading.Thread(target=requests.post("http://"+idsip+"/suricata/restart", timeout=2), name='T1')
                thread1.start()
            except Exception as e:
                pass
            suricata_status = "Deleting"
            #CMDresult = "Deleting rule"
            time.sleep(5)
            try:
                rlist = json.loads(requests.post("http://"+idsip+"/suricata/list", timeout=2).content.decode('utf-8'))
            except Exception as e:
                rlist = []
            return render(request, 'ids.html',{"rlt":CMDresult,'suricata_list':rlist,})

        elif request.POST.get('check'):
            try :
                r = json.loads(requests.post("http://"+idsip+"/suricata/status", timeout=3).content.decode('utf-8'))
            except Exception as e:
                r = {"status":False}
            rlist = []
            if {'status': True} == r :
                try:
                    rlist = json.loads(requests.post("http://"+idsip+"/suricata/list", timeout=2).content.decode('utf-8'))
                except Exception as e:
                    rlist = []
            return render(request, 'ids.html',{"status":r,'suricata_list':rlist,})
        elif request.POST.get('checkrule'):
            CMDresult = "Unknow"
            r = {"status":"Unknow"}
            comm = request.POST['command']
            post_data = {"comm":comm}
            rlist = []
            try :
                r = json.loads(requests.post("http://"+idsip+"/suricata/check-rule",post_data, timeout=3).content.decode('utf-8'))
            except Exception as e:
                r = {"status":False}
            if {"status":True} == r:
                CMDresult = "It is a vaild rule"
            else:
                CMDresult = "It is an invaild rule"
            try:
                rlist = json.loads(requests.post("http://"+idsip+"/suricata/list", timeout=2).content.decode('utf-8'))
            except Exception as e:
                rlist = []
            return render(request, 'ids.html',{"rlt":CMDresult,'suricata_list':rlist,})
        elif request.POST.get('restart'):
            #global suricata_status
            CMDresult = "Unknow"
            try:
                thread1 = threading.Thread(target=requests.post("http://"+idsip+"/suricata/restart", timeout=2), name='T1')
                thread1.start()
            except Exception as e:
                pass
            suricata_status = "Restarting"
            CMDresult = "Restarting"
            time.sleep(5)
            rlist = []
            if True :
                try:
                    rlist = json.loads(requests.post("http://"+idsip+"/suricata/list", timeout=2).content.decode('utf-8'))
                except Exception as e:
                    rlist = []
            return render(request, 'ids.html',{"rlt":CMDresult,'suricata_list':rlist,})
        elif request.POST.get('start'):
            try :
                r = json.loads(requests.post("http://"+idsip+"/suricata/start", timeout=3).content.decode('utf-8'))
                time.sleep(1)
                r = json.loads(requests.post("http://"+idsip+"/suricata/status", timeout=3).content.decode('utf-8'))
            except Exception as e:
                r = {"status":False}
            return render(request,'ids.html',{"start":r,})
        elif request.POST.get('send'):
            CMDresult = "Unknow"
            comm = request.POST['command']
            post_data = {"comm":comm}
            rlist = []
            crr = {'status': "Unknow"}
            ar = {'status': "Unknow"}
            try :
                crr = json.loads(requests.post("http://"+idsip+"/suricata/check-rule",post_data, timeout=3).content.decode('utf-8'))
                CMDresult = "It is a vaild rule"
            except Exception as e:
                CMDresult = "Please try again"
            if {'status': True} == crr:
                CMDresult = "It is a vaild rule"
                try:
                    ar = json.loads(requests.post("http://"+idsip+"/suricata/add-rule",post_data).content.decode('utf-8'))
                except Exception as e:
                    ar = {'status': False}
            else:
                CMDresult = "It is an invaild rule"
            if {"status":True} == ar:
                try:
                    thread1 = threading.Thread(target=requests.post("http://"+idsip+"/suricata/restart", timeout=2), name='T1')
                    thread1.start()
                except Exception as e:
                    pass
                suricata_status = "Adding"
                CMDresult = "Adding rule : "+comm+" successfully"
            else:
                suricata_status = ""
            time.sleep(5)
            try:
                rlist = json.loads(requests.post("http://"+idsip+"/suricata/list", timeout=2).content.decode('utf-8'))
            except Exception as e:
                rlist = []
            return render(request, 'ids.html',{"rlt":CMDresult,'suricata_list':rlist,})

        elif request.POST.get('update'):
            #global suricata_status
            CMDresult = "Unknow"
            r = {"status":"Unknow"}
            rlist = []
            try :
                r = json.loads(requests.post("http://"+idsip+"/suricata/update").content.decode('utf-8'))
            except Exception as e:
                r = {"status":False}
            if {'status':True} == r:
                try:
                    thread1 = threading.Thread(target=requests.post("http://"+idsip+"/suricata/restart", timeout=2), name='T1')
                    thread1.start()
                except Exception as e:
                    pass
                suricata_status = "Updating"
                CMDresult = "Update successfully"
            else:
                suricata_status = ""
                CMDresult = "Update unsuccessfully"
            time.sleep(5)
            if {'status': True} == r :
                try:
                    rlist = json.loads(requests.post("http://"+idsip+"/suricata/list", timeout=2).content.decode('utf-8'))
                except Exception as e:
                    rlist = []
            return render(request, 'ids.html',{"rlt":CMDresult,'suricata_list':rlist,})
    else:
        return render(request, 'ids.html',{})

