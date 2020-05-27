def getobjectgroups(DATA) -> list:
    result = list()
    ogroup = dict()
    ogroup['items'] = list()
    ogroup_detected = False
    for _ in DATA:
        data = _.strip().split()
        if len(data) == 0:
            continue
        if data[0] == "object-group":
            ogroup_detected = True
            ogroup["name"] = data[2]
            ogroup["type"] = data[1]
        if ogroup_detected:
            if data[0] == "!":
                result.append(ogroup)
                ogroup = dict()
                ogroup['items'] = list()
                ogroup_detected = False
            else:
                if data[0] == "description":
                    ogroup["description"] = ' '.join(map(str, data[1:]))
                if data[0] == "host":
                    ogroup['items'].append(("host", data[1]))
                if data[0] == "group-object":
                    ogroup['items'].append(("group-object", data[1]))
                if data[0][0].isdigit():
                    ogroup['items'].append(("network", data[0], data[1]))
    return result
