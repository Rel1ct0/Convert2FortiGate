def getObjectGroups(DATA) -> dict:
    result = dict()
    ogroup_name = ""
    ogroup_params = dict()
    ogroup_params['items'] = list()
    ogroup_detected = False
    for _ in DATA:
        data = _.strip().split()
        if len(data) == 0:
            continue
        if data[0] == "object-group":
            ogroup_detected = True
            ogroup_name = data[2]
            ogroup_params["type"] = data[1]
            # print("object detected", data[1])
        if ogroup_detected:
            if data[0] == "!":
                result[ogroup_name] = ogroup_params
                # print("Adding config for object", object_name)
                ogroup_name = ""
                ogroup_params = dict()
                ogroup_params['items'] = list()
                ogroup_detected = False
            else:
                if data[0] == "description":
                    ogroup_params["description"] = ' '.join(map(str, data[1:]))
                if data[0] == "host":
                    ogroup_params['items'].append(("host", data[1]))
                if data[0] == "group-object":
                    ogroup_params['items'].append(("group-object", data[1]))
                if data[0][0].isdigit():
                    ogroup_params['items'].append(("network", data[0], data[1]))
    return result
