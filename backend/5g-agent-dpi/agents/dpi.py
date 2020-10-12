#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import json
from pprint import pprint
from urllib import request
from urllib import parse
from http import cookiejar

def dpirt(command):
    print(command)
    os.system(command)
    return True

def status():
    try:
        os.popen("pidof ntopng").readlines()[0]
    except IndexError:
        return False
    else:
        return True
    
