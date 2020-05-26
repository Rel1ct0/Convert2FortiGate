def getInterfaces(DATA) -> dict:
    result = dict()
    interface_name = ""
    interface_params = dict()
    interface_detected = False
    for _ in DATA:
        data = _.strip().split()
        if len(data) == 0:
            continue
        if data[0] == "interface":
            interface_detected = True
            interface_name = data[1]
            # print("Interface detected", data[1])
        if interface_detected:
            if data[0] == "!":
                if not interface_params.get("shutdown"):
                    interface_params["shutdown"] = False
                result[interface_name] = interface_params
                # print("Adding config for interface", interface_name)
                interface_name = ""
                interface_params = dict()
                interface_detected = False
            else:
                if data[0] == "vlan":
                    interface_params["vlan"] = data[1]
                if data[0] == "ip" and data[1] == "address":
                    interface_params["ip"] = data[2]
                    interface_params["netmask"] = data[3]
                if data[0] == "shutdown":
                    interface_params["shutdown"] = True
    return result
