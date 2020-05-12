"""Reads input config and converts in into Dict"""


import Scripts.ASA as ASA
import Scripts.IOS as IOS


SUPPORTED_FWTYPES = ['1', 'asa', '2', 'ios']


def parseconfig(DATA, FWTYPE) -> dict:
    if FWTYPE not in SUPPORTED_FWTYPES:
        print('Unknown firewall type', FWTYPE)
        exit()

    result = dict()

    if FWTYPE in SUPPORTED_FWTYPES[0:2]:
        result["interfaces"] = ASA.getinterfaces(DATA)
    if FWTYPE in SUPPORTED_FWTYPES[2:4]:
        result["interfaces"] = IOS.getinterfaces(DATA)

    return result
