"""Reads input config and converts in into Dict"""


from Scripts.ASA import ASAParseConfig
from Scripts.IOS import IOSParseConfig


SUPPORTED_FWTYPES = ['1', 'ASA', '2', 'IOS']


def parseconfig(DATA, FWTYPE) -> dict:
    if FWTYPE not in SUPPORTED_FWTYPES:
        print('Unknown firewall type', FWTYPE)
        exit()

    result = dict()

    if FWTYPE in SUPPORTED_FWTYPES[0:2]:
        result["interfaces"] = ASAParseConfig.getinterfaces(DATA)
    if FWTYPE in SUPPORTED_FWTYPES[2:4]:
        result["interfaces"] = IOSParseConfig.getinterfaces(DATA)

    return result
