#! /usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import sys
from idstools import rule
import threading

def idsrt(command):
    print(command)
    os.system(command)
    return True

def delete(rule):
    status = "Unknow"
    delRule = rule
    result = 1

    file_path = "/var/lib/5g-agent/suricata-tmp-rule.rules"
    try:  
      f = open(file_path,'r+')  
      all_lines = f.readlines()  
      f.seek(0)  
      f.truncate()  
      for line in all_lines:
        if line.strip() != delRule.strip():
          f.write(line)  
      f.close()
      result = 0
    except IOError:  
      pass

    ####
    file_path = "/var/lib/5g-agent/suricata-tmp-rule.yaml"
    try:  
      f = open(file_path,'r+')  
      all_lines = f.readlines()  
      f.seek(0)  
      f.truncate()  
      for line in all_lines:
        if line.strip() != delRule.strip():
          f.write("- "+line)  
      f.close()
      result = 0
    except IOError:  
      pass
    ####
    status = "Deleted"
    if result == 1:
        status = False
    else:
        status = True
    return status

def list(request):
    List = []
    id = 0
    try:
        f = open("/var/lib/5g-agent/suricata-tmp-rule.rules" , 'r+')
    except IOError:
        pass
    for line in f:
        id += 1
        List.append({"id":id, "rule":line})
    return List

def status():
    try:
        os.popen("pidof suricata").readlines()[0]
    except IndexError:
        return False
    else:
        return True


def parse_custom_rule(custom_rule):
    r = rule.parse(custom_rule)
    if str(r) == "None":
        return False
    return True


def add_custom_rule(custom_rule):
    r = rule.parse(custom_rule)
    if str(r) == "None":
        return False
    if not os.path.exists("/var/lib/5g-agent"):
        os.makedirs("/var/lib/5g-agent")
    f = open("/var/lib/5g-agent/suricata-tmp-rule.rules", "a")
    f.write(str(r) + "\n")
    f.close()
    ###
    f = open("/var/lib/5g-agent/suricata-tmp-rule.yaml", "a")
    f.write(str(r) + "\n")
    f.close()
    ###
    os.system("sudo suricata-update remove-source 5g/custom")
    os.system("sudo suricata-update add-source 5g/custom file:///var/lib/5g-agent/suricata-tmp-rule.rules")
    os.system("sudo suricata-update -f")
    return True


def restart_suricata():
    thread1 = threading.Thread(target=os.system("sudo systemctl force-reload suricata"), name='T1')
    thread1.start()
    return True

def update():
    os.system("sudo suricata-update")
    return True
