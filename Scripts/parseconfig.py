"""Reads input config and converts in into Dict"""


import Scripts.ASA as ASA
import Scripts.IOS as IOS
import Scripts.FortiGate as FortiGate


SUPPORTED_FWTYPES = ['1', 'asa', '2', 'ios']


def parseconfig(RAWDATA, FWTYPE) -> dict:
    if FWTYPE not in SUPPORTED_FWTYPES:
        print('Unknown firewall type', FWTYPE)
        exit()

    result = dict()

    if FWTYPE in SUPPORTED_FWTYPES[0:2]:
        result["interfaces"] = ASA.getinterfaces(RAWDATA)
    if FWTYPE in SUPPORTED_FWTYPES[2:4]:
        result["interfaces"] = IOS.getinterfaces(RAWDATA)
        result["zones"] = IOS.getzones(result["interfaces"])
        result["object-groups"] = IOS.getobjectgroups(RAWDATA)
        result["acls"] = IOS.getacls(RAWDATA)

    return result


def createconfig(STRUCTDATA) -> str:
    result = str()
    result = result + FortiGate.setinterfaces(STRUCTDATA)
    result = result + FortiGate.setzones(STRUCTDATA)
    objectgroups = FortiGate.setobjectgroups(STRUCTDATA)
    objects = FortiGate.setobjects(STRUCTDATA)
    result = result + objects
    result = result + objectgroups
    return result
