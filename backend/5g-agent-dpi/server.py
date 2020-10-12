#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import json
import os

from agents import dpi

from flask import Flask,redirect
from flask import request
from flask import session
from flask import jsonify

app = Flask(__name__)

@app.route('/ntopng/rt',methods=['GET','POST'])
def rt():
    status = "Unknow"
    if request.method == 'POST' :
        command = request.form['command']
        print(command)
        status = dpi.dpirt(command)
        return json.dumps({"status":status})
    else:
        return '{"status":"error"}'

@app.route('/ntopng/status',methods=['GET','POST'])
def check_ntopng():
    status = dpi.status()
    obj = {
        "status": status
    }
    return json.dumps(obj)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port='3500')
