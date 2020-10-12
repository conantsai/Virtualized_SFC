#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import json
from pprint import pprint
from urllib import request
from urllib import parse
from http import cookiejar

def natrt(command):
    #print(command)
    os.system(command)
    return True

def nattraceroute(command):
    orderlist = ""
    for line in os.popen(command.split("/")[0]):
        orderlist = orderlist + line.split("(")[1].split(")")[0] + ">"
    return orderlist

def rulelist(command):
    list = []
    for sfc_info in os.popen(command):
        order = ""
        natport = sfc_info.split(":proto=", 1)[0].split("port=", 1)[1]
        srvport = sfc_info.split(":toaddr=", 1)[0].split("toport=", 1)[1]
        srvip = sfc_info.split("toaddr=", 1)[1].split("\n", 1)[0] 

        for sfc_order in os.popen("traceroute " + srvip):
            print(sfc_order)
            order = order + sfc_order.split("(")[1].split(")")[0] + ">"
        list.append({"natport": natport,
                     "srvport": srvport,
                     "srvip": srvip,
                     "order": order})                   
    return list
