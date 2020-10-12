#! /usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import getpass

def wafrt(command):
    print(command)
    os.system(command)
    return True

def delete(rule):
    os.system("touch /usr/local/nginx/conf/custom.conf")
    os.system("sudo cp /usr/local/nginx/conf/custom.conf /usr/local/nginx/conf/custom_cp.conf")
    os.system("sudo cp /usr/local/nginx/conf/modsec_includes.conf /usr/local/nginx/conf/modsec_includes_cp.conf")

    status = "Unknow"
    delRule = rule
    result = 1

    file_path = "/usr/local/nginx/conf/custom.conf"
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

    status = "Deleted"
    if result == 1:
        status = False
    else:
        status = True
    return status

def modseclist(request):
    List = []
    id = 0
    try:
        f = open("/usr/local/nginx/conf/custom.conf" , 'r+')
    except IOError:
        pass
    for line in f:
        id += 1
        List.append({"id":id, "rule":line})
    return List

def nginx_status():
    try: 
        os.popen("ps -C nginx | grep -v CMD | awk '{print $1}'").readlines()[0]
    except IndexError:
        return False
    else:
        return True

def nginx_modsecurity():
    TEMP_FILE_PATH = "./tempf"
    try: 
        os.popen("ps -C nginx | grep -v CMD | awk '{print $1}'").readlines()[0]
    except IndexError:
        return False
    s = os.popen("ps -C nginx | grep -v CMD | awk '{print $1}'").readlines()[0]
    s = "ls -l /proc/" + s[:s.find("/n")] + "/exe > " + TEMP_FILE_PATH  
    os.system(s)
    f = open(TEMP_FILE_PATH , 'r')
    s = f.readline()
    f.close()
    s = s[s.find('>')+2:-1] + " -V 2> " + TEMP_FILE_PATH
    os.popen(s)
    f = open(TEMP_FILE_PATH , 'r')
    for line in f:
        if line.find('modsecurity') != -1:
            return False
    return True

def mod_custom_rule(cmd):
    os.system("touch /usr/local/nginx/conf/custom.conf")
    os.system("sudo cp /usr/local/nginx/conf/custom.conf /usr/local/nginx/conf/custom_cp.conf")
    os.system("sudo cp /usr/local/nginx/conf/modsec_includes.conf /usr/local/nginx/conf/modsec_includes_cp.conf")
    try:
        f = open("/usr/local/nginx/conf/modsec_includes.conf" , 'r+')
    except IOError:
        return False
    boolean = 0
    for line in f:
        if line == "include custom.conf\n":
            boolean = 1
    if boolean == 0:
        f.write("include custom.conf\n")
    f.close()
    f = open("/usr/local/nginx/conf/custom.conf", 'a')
    f.write(cmd + "\n")
    f.close
    return True

def stop_nginx():
    os.system("sudo systemctl stop nginx.service")
    return True

def restart_nginx():
    os.system("sudo systemctl restart nginx.service")
    return True
