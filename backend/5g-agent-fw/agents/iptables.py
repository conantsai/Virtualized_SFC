#! /usr/bin/env python3
#-*- coding:utf-8 -*-
import iptc
import shlex

import os
import json
from pprint import pprint
from urllib import request
from urllib import parse
from http import cookiejar

def fwrt(command):
    print(command)
    os.system(command)
    return True

def iptables_status():
    if os.system('iptables -V') == 0:
        return True
    else:
        return False
def fwlist():
    List = []
    tables = { "filter": { "chain": "FORWARD" }, "mangle": { "chain": "PREROUTING" } }
    for table in tables:
        tables[table]["table"] = iptc.Table(table)
        tables[table]["table"].refresh()
        userInput = iptc.Chain(tables[table]["table"], "user_input")
        id = 0
        for rule in userInput.rules:
            id += 1
            if len(rule.matches) == 0:
                List.append({"id":table[0]+tables[table]["chain"][0:2].lower()+str(id), "table": table, "chain_name":tables[table]["chain"], "target":rule.target.name, "protocol":rule.protocol, "src":rule.src, "dst":rule.dst, "interface_in":rule.in_interface, "interface_out":rule.out_interface, "matches":"None"})
            else:
                matches = {}
                for match in rule.matches:
                    matches[match.name] = []
                    for key, value in match.parameters.items():
                        matches[match.name].append({ key: value })
                List.append({"id":table[0]+tables[table]["chain"][0:2].lower()+str(id), "table": table, "chain_name":tables[table]["chain"], "target":rule.target.name, "protocol":rule.protocol, "src":rule.src, "dst":rule.dst, "interface_in":rule.in_interface, "interface_out":rule.out_interface, "matches":matches})
    return List 

def delete(id):
    if id[:3] == "ffo":
        cmd = "iptables -D user_input " + id[3:]
    elif id[:3] == "mpr":
        cmd = "iptables -t mangle -D user_input " + id[3:]
    else:
        cmd = "exit 1"

    result = os.system(cmd)

    if result == 0:
        os.system("iptables-save > iptables.conf")
        status = True
    else:
        status = False
    return status

def adding(mTable, mProt, mSourIP, mDestIP, mSourPort, mDestPort, mTarget, mOptions):
    status = "Unknow"
    addTable = mTable
    addChain = "user_input"
    addTarget = mTarget
    addPort = mProt
    addSrc = mSourIP
    addSp = mSourPort
    addDst = mDestIP
    addDp = mDestPort
    addOpts = mOptions

    mTable = shlex.quote(mTable)
    addTarget = shlex.quote(addTarget)
    addPort = shlex.quote(addPort)
    addSrc = shlex.quote(addSrc)
    addSp = shlex.quote(addSp)
    addDst = shlex.quote(addDst)
    addDp = shlex.quote(addDp)
    addOpts = shlex.quote(addOpts)

    result = 1

    CMDS = ""
    CMDD = ""
    if not addSrc == "''" :
        CMDS = " -s "+addSrc + " "
    if not addDst == "''" :
        CMDD = " -d "+addDst + " "

    CMDSp = ""
    CMDDp = ""
    if not addSp == "''":
        CMDSp = " --sport "+addSp + " "
    if not addDp == "''":
        CMDDp = " --dport "+addDp + " "

    if addOpts == "''" or addOpts != ("'" + mOptions + "'"):
        addOpts = ""
    else:
        addOpts = " " + addOpts[1:-1]

    os.system("iptables -t " + addTable + " -A " + addChain + " -p " + addPort + CMDS + CMDSp + CMDD + CMDDp + addOpts + " -j " + addTarget)
    status = "Added"
    result = os.system("iptables -t " + addTable + " -C " + addChain + " -p " + addPort + CMDS + CMDSp + CMDD + CMDDp + addOpts + " -j " + addTarget)
    if result == 0:
        os.system("iptables-save > iptables.conf")
        status = True
    else:
        status = False
    return status
