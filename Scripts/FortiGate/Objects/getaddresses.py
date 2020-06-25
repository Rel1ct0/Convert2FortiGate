def getaddresses(DATA: dict):
    for interface, iface_params in DATA.get('interfaces').items():  # Check all interfaces
        if acl := iface_params.get('acl-in'):  # Check applied ACLs
            for counter in range(0, len(DATA['acls'][acl])):  # For every line
                if DATA['acls'][acl][counter].get('dst') and DATA['acls'][acl][counter]['dst'].get('ip'):
                    if DATA['acls'][acl][counter]['dst']['ip'] == 'any':
                        DATA['acls'][acl][counter]['dst']['object'] = 'all'
                    else:  # Not any
                        name = str()
                        if DATA['acls'][acl][counter]['dst']['mask'] == '255.255.255.255':
                            name = name + 'Host_'
                        else:
                            name = name + 'Net_'
                        name = name + DATA['acls'][acl][counter]['dst']['ip'] + '_' + DATA['acls'][acl][counter]['dst']['mask']
                        if not DATA['objects']['address'].get(name):  # This object does not exist, create it
                            DATA['objects']['address'][name] = dict()
                            DATA['objects']['address'][name]['prefix'] = DATA['acls'][acl][counter]['dst']['ip']
                            DATA['objects']['address'][name]['mask'] = DATA['acls'][acl][counter]['dst']['mask']
                        DATA['acls'][acl][counter]['dst']['object'] = name
                if DATA['acls'][acl][counter].get('src') and DATA['acls'][acl][counter]['src'].get('ip'):
                    if DATA['acls'][acl][counter]['src']['ip'] == 'any':
                        DATA['acls'][acl][counter]['src']['object'] = 'all'
                    else:  # Not any
                        name = str()
                        if DATA['acls'][acl][counter]['src']['mask'] == '255.255.255.255':
                            name = name + 'Host_'
                        else:
                            name = name + 'Net_'
                        name = name + DATA['acls'][acl][counter]['src']['ip'] + '_' + DATA['acls'][acl][counter]['src']['mask']
                        if not DATA['objects']['address'].get(name):  # This object does not exist, create it
                            DATA['objects']['address'][name] = dict()
                            DATA['objects']['address'][name]['prefix'] = DATA['acls'][acl][counter]['src']['ip']
                            DATA['objects']['address'][name]['mask'] = DATA['acls'][acl][counter]['src']['mask']
                        DATA['acls'][acl][counter]['src']['object'] = name
    return