#!/usr/bin/env python3
"""Converts firewall configuration into compatible FortiGate"""


import sys
from Scripts import parseconfig
import pprint

if len(sys.argv) == 1 or len(sys.argv) > 4:
    print('Usage: Convert2FortiGate.py <fwtype> <asaconfig.txt> [fgateconfig.txt]')
    print("Supported firewall types are:")
    print("1. ASA")
    print("2. IOS")
    exit()

if len(sys.argv) == 4:
    OUTFILE = sys.argv[3]
else:
    OUTFILE = "fgateconfig.txt"

FWTYPE = sys.argv[1]

try:
    with open(sys.argv[2]) as INPUTFILE:
        INPUTDATA = INPUTFILE.readlines()
except Exception as error:
    print("Can not open", sys.argv[1], "for reading, got", error)
    exit()

ConfigDict = parseconfig.parseconfig(INPUTDATA, FWTYPE.lower())
ConvertedConfig = parseconfig.createconfig(ConfigDict)

with open('rawrict.txt', 'w') as raw:
    raw.write(pprint.pformat(ConfigDict))

try:
    with open(OUTFILE, 'w') as OUTPUTFILE:
        OUTPUTFILE.write(ConvertedConfig)
        #OUTPUTFILE.write(str(ConfigDict))
except Exception as error:
    print("Can not open", OUTFILE, "for writing, got", error)
    exit()

#pprint.pprint(ConfigDict)
#pprint.pprint(parseconfig.createconfig(ConfigDict))
