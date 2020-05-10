#!/usr/bin/env python3
"""Converts ASA firewall configuration into compatible FortiGate"""


import sys
from Scripts import parseconfig
import pprint

if len(sys.argv) == 1:
    print("Usage: ASA2FortiGate.py <asaconfig>.txt [fgateconfig.txt]")
    exit()

if len(sys.argv) == 3:
    OUTFILE = sys.argv[2]
else:
    OUTFILE = "fgateconfig.txt"

try:
    with open(sys.argv[1]) as INPUTFILE:
        INPUTDATA = INPUTFILE.readlines()
except Exception as error:
    print("Can not open", sys.argv[1], "for reading, got", error)
    exit()

ConfigDict = parseconfig.parseconfig(INPUTDATA)

pprint.pprint(ConfigDict)
