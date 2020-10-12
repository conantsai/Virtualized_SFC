#! /usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import json
from pprint import pprint
from urllib import request
from urllib import parse
from http import cookiejar

def gwrt(command):
    print(command)
    os.system(command)
    return True
    
