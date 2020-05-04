#!/usr/bin/env python3
"""Converts ASA firewall configuration into compatible FortiGate"""


import sys
import os

if len(sys.argv)==1:
    print("Usage: ASA2FortiGate.py <asaconfig>.txt [fgateconfig.txt]")
    exit()


