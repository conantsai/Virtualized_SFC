#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import json
import os

from agents import suricata

from flask import Flask
from flask import request
from flask import session
from flask import jsonify

app = Flask(__name__)

@app.route('/suricata/rt',methods=['GET','POST'])
def rt():
    status = "Unknow"
    if request.method == 'POST' :
        command = request.form['command']
        print(command)
        status = suricata.idsrt(command)
        return json.dumps({"status":status})
    else:
        return '{"status":"error"}'

@app.route('/suricata/delete',methods=['GET','POST'])
def delete():
    status = "Unknow"
    if request.method == 'POST' :
        rule = request.form['rule']
        status = suricata.delete(rule)
    obj = {
        "status": status
    }
    return json.dumps(obj)

@app.route('/suricata/list',methods=['GET','POST'])
def idslist():
    if request.method == 'POST' :
        return json.dumps(suricata.list(request))
    else:
        return '{"status":true}'


@app.route('/suricata/status',methods=['GET','POST'])
def check_suricata():
    if request.method == 'POST' :
        status = suricata.status()
        obj = {
            "status": status
        }
        return json.dumps(obj)


@app.route('/suricata/check-rule',methods=['GET','POST'])
def suricata_check_rule():
    if request.method == 'POST' :
        rule = request.form["comm"]
        status = suricata.parse_custom_rule(rule)
        obj = {
            "status": status
        }
        return json.dumps(obj)


@app.route('/suricata/add-rule',methods=['GET','POST'])
def suricata_add_rule():
    if request.method == 'POST' :
        rule = request.form["comm"]
        status = suricata.add_custom_rule(rule)
        obj = {
            "status": status
        }
    return json.dumps(obj)


@app.route('/suricata/restart',methods=['GET','POST'])
def suricata_restart():
    status = "Unknow"
    if request.method == 'POST' :
        suricata.restart_suricata()
        status = True
    else:
        status = "method is GET"
    obj = {
        "status": status
    }
    return json.dumps(obj)


@app.route('/suricata/start',methods=['GET','POST'])
def suricata_start():
  if request.method == 'POST' :
    status = '{"status":True}'
    os.system('sudo iptables -I INPUT -j NFQUEUE')
    os.system('sudo iptables -I OUTPUT -j NFQUEUE')
    os.system('sudo systemctl start suricata')
    return json.dumps(status)

@app.route('/suricata/update',methods=['GET','POST'])
def suricata_update():
    status = "Unknow"
    if request.method == 'POST' :
        status = suricata.update()
        obj = {
            "status": status
        }
    return json.dumps(obj)

@app.route('/status',methods=['GET','POST'])
def server_status():
    return '{"status": true}'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port='6002')
