#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import json
import os
import time

from agents import modsec

from flask import Flask
from flask import request
from flask import session
from flask import jsonify

app = Flask(__name__)

@app.route('/modsec/rt',methods=['GET','POST'])
def rt():
    status = "Unknow"
    if request.method == 'POST' :
        command = request.form['command']
        print(command)
        status = modsec.wafrt(command)
        return json.dumps({"status":status})
    else:
        return '{"status":"error"}'

@app.route('/modsec/list',methods=['GET','POST'])
def list():
    if request.method == 'POST' :
        return json.dumps(modsec.modseclist(request))
    else:
        return '{"status":true}'
	
@app.route('/modsec/status',methods=['GET','POST'])
def status():
    status = False
    if request.method == 'POST' :
        nginx_status = modsec.nginx_status()
        modsec_status = modsec.nginx_modsecurity()
        if nginx_status == True and modsec_status == True:
            status = True
    else:
        pass
    obj = {
        "status": status
    }
    return json.dumps(obj)
@app.route('/modsec/nginx-status',methods=['GET','POST'])
def check_nginx():
    status = False
    if request.method == 'POST' :
        status = modsec.nginx_status()
    else:
        pass
    obj = {
        "status": status
    }
    return json.dumps(obj)


@app.route('/modsec/nginx-modsec',methods=['GET','POST'])
def check_nginx_modsec():
    status = False
    if request.method == 'POST' :
        status = modsec.nginx_modsecurity()
    else:
        pass
    obj = {
        "status": status
    }
    return json.dumps(obj)


@app.route('/modsec/add-rule',methods=['GET','POST'])
def modsec_add_rule():
    status = "Unknow"
    cmdstatus = False
    modsecadd_status = False
    if request.method == 'POST' :
        rule = request.form["comm"]
        cmdstatus = modsec.mod_custom_rule(rule)
        
        if cmdstatus == True:
            status = "add rule successful but not test yet"
            modsec.restart_nginx()
            time.sleep(7)
            
            modsecadd_status = modsec.nginx_status()
            if modsecadd_status == True:
                
                status = True
            else:
                status = "invaild cmd"
                os.system("sudo cp /usr/local/nginx/conf/custom_cp.conf /usr/local/nginx/conf/custom.conf")
                os.system("sudo cp /usr/local/nginx/conf/modsec_includes_cp.conf /usr/local/nginx/conf/modsec_includes.conf")
                
                modsec.restart_nginx()
                time.sleep(7)
                recovery = modsec.nginx_status()
                if recovery == True:
                    status = "invaild cmd but recovery"
                else:
                    status = "invaild cmd and recovery failed"
        else:
            status = "add rule failed"
        
    obj = {
        "status": status
    }
    
    return json.dumps(obj)


@app.route('/modsec/nginx-restart',methods=['GET','POST'])
def modsec_restart():
    status = False
    if request.method == 'POST' :
        status = modsec.restart_nginx()
        
    else:
        pass
    obj = {
        "status": status
    }
    return json.dumps(obj)

@app.route('/modsec/delete',methods=['GET','POST'])
def delete():
    status = "Unknow"
    if request.method == 'POST' :
        rule = request.form['rule']
        status = modsec.delete(rule)

        if status == True:
            status = "delete rule successful but not test yet"
            modsec.restart_nginx()
            time.sleep(7)

            modsecadd_status = modsec.nginx_status()
            if modsecadd_status == True:
                status = True
            else:
                status = "invaild delete"
                os.system("sudo cp /usr/local/nginx/conf/custom_cp.conf /usr/local/nginx/conf/custom.conf")
                os.system("sudo cp /usr/local/nginx/conf/modsec_includes_cp.conf /usr/local/nginx/conf/modsec_includes.conf")

                modsec.restart_nginx()
                time.sleep(7)
                recovery = modsec.nginx_status()
                if recovery == True:
                    status = "invaild delete but recovery"
                else:
                    status = "invaild delete and recovery failed"
        else:
            status = "delete rule failed"

    obj = {
        "status": status
    }
    return json.dumps(obj)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port='7000')
