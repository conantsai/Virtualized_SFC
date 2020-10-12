#!/bin/bash
cd "$(dirname ${BASH_SOURCE[0]})"
iptables-restore -T filter -n < iptables.conf
iptables-restore -T mangle -n < iptables.conf
./server.py
