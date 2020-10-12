#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import json
import os

from agents import iptables

from flask import Flask
from flask import request
from flask import session
from flask import jsonify

app = Flask(__name__)

@app.route('/iptables/rt',methods=['GET','POST'])
def rt():
    status = "Unknow"
    if request.method == 'POST' :
        command = request.form['command']
        print(command)
        status = iptables.fwrt(command)
        return json.dumps({"status":status})
    else:
        return '{"status":"error"}'

@app.route('/iptables/status',methods=['GET','POST'])
def iptables_status():
    status = False
    if request.method == 'POST' :
        status = iptables.iptables_status()
    obj = {
        "status": status
    }
    return json.dumps(obj)

@app.route('/iptables/fwlist',methods=['GET','POST'])
def fwlist():
  if request.method == 'POST' :
    return json.dumps(iptables.fwlist())
  else:
    return '{"status":true}'
	
@app.route('/iptables/delete',methods=['GET','POST'])
def delete():
    status = "Unknow"
    if request.method == 'POST' :
        status = iptables.delete(request.form['id'])
    obj = {
        "status": status
    }
    return json.dumps(obj)

@app.route('/iptables/adding',methods=['GET','POST'])
def adding():
    status = False
    if request.method == 'POST' :
        mTable = request.form['table']
        mProt = request.form['protocol']
        mSourIP = request.form['fromip']
        mDestIP = request.form['toip']
        mSourPort = request.form['fromport']
        mDestPort = request.form['toport']
        mTarget = request.form['target']
        mOptions = request.form['options']

        status = iptables.adding(mTable, mProt, mSourIP, mDestIP, mSourPort, mDestPort, mTarget, mOptions)
        obj = {
            "status": status
        }
        return json.dumps(obj)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port='5000')
