"""Reads input config and converts in into Dict"""

from Scripts import interfaces


def parseconfig(DATA) -> dict:
    result = dict()
    result["interfaces"] = interfaces.getinterfaces(DATA)
    return result
