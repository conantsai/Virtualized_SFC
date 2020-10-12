#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import json
import os

from agents import gw

from flask import Flask,redirect
from flask import request
from flask import session
from flask import jsonify

app = Flask(__name__)

@app.route('/gw/rt',methods=['GET','POST'])
def rt():
    status = "Unknow"
    if request.method == 'POST' :
        command = request.form['command']
        print(command)
        status = gw.gwrt(command)
        return json.dumps({"status":status})
    else:
        return '{"status":"error"}'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port='5000')
