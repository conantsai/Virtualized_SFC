from datetime import datetime
from django.shortcuts import render
import requests
import json
from board.views import fwip
from board.views import idsip
from board.views import dpiip
from board.views import wafip

from board.views import natip
from board.views import gwip

def chain(request):
    orderlist = [None]*4

    myOrderlist = []

    service_domain = "172.17.1.0/24"
    service2_domain = "172.17.2.0/24"
    nat_address = "172.17.0.253"
    gw_address = "172.17.0.3"
    gw_address2 = "172.17.1.254"
    fw_address = "172.17.0.201"
    ids_address = "172.17.0.202"
    dpi_address = "172.17.0.203"
    waf_address = "172.17.0.204"

    fw_interface = "ens192"
    ids_interface = "ens192"
    dpi_interface = "ens192"
    waf_interface = "ens192"
    nat_interface = "ens192"
    gw_interface = "ens192"

    fw_order = -1
    ids_order = -1
    dpi_order = -1
    waf_order = -1
    
    nat_command = ""
    fw_command = ""
    ids_command = ""
    dpi_command = ""
    waf_command = ""
    gw_command = ""

    nat_check_r = ""

    nat_check_command = "traceroute "+gw_address2
    nat_check_post_data = {"command":nat_check_command}
    nat_check_r = {"order":"unknow"}
    try :
        nat_check_r = json.loads(requests.post("http://"+natip+"/nat/traceroute", nat_check_post_data,timeout=30).content.decode('utf-8'))
        nat_check_r['order'] = nat_check_r['order'].replace(fw_address,"FW").replace(ids_address,"IDS").replace(dpi_address,"DPI").replace(waf_address,"WAF").replace(gw_address2+">","").replace(">"+gw_address+">"+gw_address+">","")

    except Exception as e:
        nat_check_r = {"order":"false"}

    # 獲得網路服務排序 
    if request.method == "POST":
        myOrderlist.append(nat_address)
        for i in range(len(orderlist)):
            i = str(i)
            service = request.POST['sel' + i] 
            i = int(i)

            if service == "不執行":

                continue
            else:
                if i == 0:
                    service = int(service) - 1
                    orderlist[service] = []
                    orderlist[service].append("FW")
                    orderlist[service].append(fw_address)
                elif i == 1:
                    service = int(service) - 1
                    orderlist[service] = []
                    orderlist[service].append("IDS")
                    orderlist[service].append(ids_address)
                elif i == 2:
                    service = int(service) - 1
                    orderlist[service] = []
                    orderlist[service].append("DPI")
                    orderlist[service].append(dpi_address)
                elif i == 3:
                    service = int(service) - 1
                    orderlist[service] = []
                    orderlist[service].append("WAF")
                    orderlist[service].append(waf_address)
    
        # 刪除多餘list
        while None in orderlist:
            orderlist.remove(None)
        for i in range(len(orderlist)):
            myOrderlist.append(orderlist[i][1])
            if(orderlist[i][1]==fw_address):
                fw_order = i+1
            elif(orderlist[i][1]==ids_address):
                ids_order = i+1
            elif(orderlist[i][1]==dpi_address):
                dpi_order = i+1
            elif(orderlist[i][1]==waf_address):
                waf_order = i+1
        myOrderlist.append(gw_address)

        if len(orderlist) == 0:
            nat_command = "sudo nmcli con modify " + nat_interface +" ipv4.routes \"" + service_domain + " " + gw_address +"\" +ipv4.routes \"" + service2_domain + " " + gw_address +" \" ; sudo systemctl restart network;"
            gw_command = "sudo nmcli con modify " + gw_interface +" ipv4.gateway \"" + nat_address + "\" ; sudo systemctl restart network;"
        else:
            nat_command = "sudo nmcli con modify " + nat_interface +" ipv4.routes \"" + service_domain + " " + myOrderlist[1] +"\" +ipv4.routes \"" + service2_domain + " " + myOrderlist[1] + "\" ; sudo systemctl restart network;"
            gw_command = "sudo nmcli con modify " + gw_interface +" ipv4.gateway \"" + myOrderlist[len(myOrderlist)-2] + "\" ; sudo systemctl restart network;"

            if(fw_order != -1):
                fw_command = "sudo nmcli con modify " + fw_interface + " ipv4.routes \"" + service_domain + " " + myOrderlist[fw_order+1] + "\" +ipv4.routes \"" + service2_domain + " " + myOrderlist[fw_order+1] + "\" ; sudo nmcli con modify " + fw_interface +" ipv4.gateway \"" + myOrderlist[fw_order-1] + "\" ; sudo systemctl restart network;"
            if(ids_order != -1):
                ids_command = "sudo nmcli con modify " + ids_interface + " ipv4.routes \"" + service_domain + " " + myOrderlist[ids_order+1] + "\" +ipv4.routes \"" + service2_domain + " " + myOrderlist[ids_order+1] + "\" ; sudo nmcli con modify " + ids_interface +" ipv4.gateway \"" + myOrderlist[ids_order-1] + "\" ; sudo systemctl restart network;"
            if(dpi_order != -1):
                dpi_command = "sudo nmcli con modify " + dpi_interface + " ipv4.routes \"" + service_domain + " " + myOrderlist[dpi_order+1] + "\" +ipv4.routes \"" + service2_domain + " " + myOrderlist[dpi_order+1] + "\" ; sudo nmcli con modify " + dpi_interface +" ipv4.gateway \"" + myOrderlist[dpi_order-1] + "\" ; sudo systemctl restart network;"
            if(waf_order != -1):
                waf_command = "sudo nmcli con modify " + waf_interface + " ipv4.routes \"" + service_domain + " " + myOrderlist[waf_order+1] + "\" +ipv4.routes \"" + service2_domain + " " + myOrderlist[waf_order+1] +  "\" ; sudo nmcli con modify " + waf_interface +" ipv4.gateway \"" + myOrderlist[waf_order-1] + "\" ; sudo systemctl restart network;"
                
        fw_post_data = {"command":fw_command}
        fwr = {"status":"unknow"}        
        ids_post_data = {"command":ids_command}
        idsr = {"status":"unknow"}
        dpi_post_data = {"command":dpi_command}
        dpir = {"status":"unknow"}
        waf_post_data = {"command":waf_command}
        wafr = {"status":"unknow"}
        try :
            fwr = json.loads(requests.post("http://"+fwip+"/iptables/rt", fw_post_data, timeout=10).content.decode('utf-8'))
        except Exception as e:
            fwr = {"status":"false"}
        try :
            idsr = json.loads(requests.post("http://"+idsip+"/suricata/rt", ids_post_data, timeout=10).content.decode('utf-8'))
        except Exception as e:
            idsr = {"status":"false"}
        try :
            dpir = json.loads(requests.post("http://"+dpiip+"/ntopng/rt", dpi_post_data, timeout=10).content.decode('utf-8'))
        except Exception as e:
            dpir = {"status":"false"}
        try :
            wafr = json.loads(requests.post("http://"+wafip+"/modsec/rt", waf_post_data, timeout=10).content.decode('utf-8'))
        except Exception as e:
            wafr = {"status":"false"}

        nat_post_data = {"command":nat_command}
        natr = {"status":"unknow"}
        gw_post_data = {"command":gw_command}
        gwr = {"status":"unknow"}
        try :
            natr = json.loads(requests.post("http://"+natip+"/nat/rt", nat_post_data, timeout=10).content.decode('utf-8'))
        except Exception as e:
            natr = {"status":"false"}
        try :
            gwr = json.loads(requests.post("http://"+gwip+"/gw/rt", gw_post_data, timeout=10).content.decode('utf-8'))
        except Exception as e:
            gwr = {"status":"false"}

        nat_check_command = "traceroute "+gw_address2
        nat_check_post_data = {"command":nat_check_command}
        nat_check_r = {"order":"unknow"}
        try :
            nat_check_r = json.loads(requests.post("http://"+natip+"/nat/traceroute", nat_check_post_data, timeout=30).content.decode('utf-8'))
            nat_check_r['order'] = nat_check_r['order'].replace(fw_address,"FW").replace(ids_address,"IDS").replace(dpi_address,"DPI").replace(waf_address,"WAF").replace(gw_address2+">","").replace(">"+gw_address+">"+gw_address+">","")

        except Exception as e:
            nat_check_r = {"order":"false"}

    else:
        serviceorder = "尚未選擇網路安全服務鏈接執行順序"

    return render(request,"SFC.html",{"result":nat_check_r['order']})#,"nat":nat_command,"fw":fw_command,"ids":ids_command,"dpi":dpi_command,"waf":waf_command,"gw":gw_command})

    #return render(request,"SFC.html",{"serviceorder":orderlist,"nat":nat_command,"fw":fw_command,"ids":ids_command,"dpi":dpi_command,"waf":waf_command,"gw":gw_command})

