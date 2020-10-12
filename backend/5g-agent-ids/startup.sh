#!/bin/bash
cd "$(dirname ${BASH_SOURCE[0]})"
sudo iptables -I INPUT -j NFQUEUE
sudo iptables -I OUTPUT -j NFQUEUE
sudo ./server.py

