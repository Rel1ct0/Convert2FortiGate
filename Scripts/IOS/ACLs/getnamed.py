def getnamed(DATA) -> dict:
    result = dict()
    for _ in DATA:
        data = _.strip().split()
        if len(data) == 0:
            continue
        if data[0] == "ip" and data[1] == "access-list":
            if data[2] == "standard":
                if not result.get(data[3]):  # First line of ACL, create it
                    result[data[3]] = list()
                asdsa
            elif data[2] == "extended":
                if not result.get(data[3]):  # First line of ACL, create it
                    result[data[3]] = list()
                dasddas
    return result
