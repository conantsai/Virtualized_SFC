from django.shortcuts import render
from django.shortcuts import redirect
import requests
import json
from board.views import fwip

def fwaddpage(request):
    return render(request,'fwaddpage.html',{})
	
def fwlist(request):
    r = []
    try :
        r = json.loads(requests.post("http://"+fwip+"/iptables/fwlist", timeout=2).content.decode('utf-8'))
    except Exception as e:
        r = []
    return render(request,'fwlist.html',{"firewall_list":r,}) 

def fwaction(request):
    if request.method == "POST":
        if request.POST.get('Delete'):
            result = "FireWall"
            successfulCounter = 0
            failedCounter = 0
            otherCounter = 0
            check_box_list = request.POST.getlist('delete')
            for id in reversed(check_box_list):
                try :
                    r = json.loads(requests.post("http://"+fwip+"/iptables/delete", { "id": id }, timeout=2).content.decode('utf-8'))
                    if {'status': True} == r:
                        successfulCounter += 1
                    elif {'status': False} == r:
                        failedCounter += 1
                    else:
                        otherCounter += 1
                except Exception as e:
                    pass
            result = str(successfulCounter) + " rule(s) delete successfully, and " + str(failedCounter + otherCounter) + " rule(s) delete failed"
            r = []
            try :
                r = json.loads(requests.post("http://"+fwip+"/iptables/fwlist", timeout=2).content.decode('utf-8'))
            except Exception as e:
                r =[]
            return render(request, 'fwlist.html', {"firewall_list":r,'result':result,'Counter':failedCounter + otherCounter})
        elif request.POST.get('AddPage'):
            return render(request, 'fwaddpage.html',{})
        elif request.POST.get('Return'):
            return redirect('/fwlist/')
        elif request.POST.get('Add'):
            counter = 1
            result = "FireWall"
            target = request.POST['target']
            table = request.POST['table']
            protocol = request.POST['protocol']
            fromip = request.POST['fromip']
            fromport = request.POST['fromport']
            toip = request.POST['toip']
            toport = request.POST['toport']
            options = request.POST['options']
            post_data = { "target": target, "table": table, "protocol": protocol, "fromip": fromip, "fromport": fromport, "toip": toip, "toport": toport, "options": options }
            re = {'status': "error"}
            try:
                re = json.loads(requests.post("http://"+fwip+"/iptables/adding",post_data, timeout=2).content.decode('utf-8'))
            except Exception as e:
                re = {'status': "error"}
            if {'status': True} == re:
                result = "Adding rule successfully"
                counter = 0
            else:
                result = "Could not Add rule, please check your parameters"
                counter = 1
            r = []
            try :
                r = json.loads(requests.post("http://"+fwip+"/iptables/fwlist", timeout=2).content.decode('utf-8'))
            except Exception as e:
                r = []
            return render(request, 'fwlist.html', {"firewall_list":r,'result':result,'Counter':counter})
    else:
        r = []
        try:
            r = json.loads(requests.post("http://"+fwip+"/iptables/fwlist",post_data, timeout=2).content.decode('utf-8'))
        except Exception as e:
            r = []
        return render(request, 'fwlist.html', {"firewall_list":r})
