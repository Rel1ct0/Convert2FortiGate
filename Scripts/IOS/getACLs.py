import Scripts.IOS.ACLs as ACLs


def getacls(DATA) -> dict:
    result = dict()
    result.update(ACLs.getnumbered(DATA))
    result.update(ACLs.getnamed(DATA))
    return result
