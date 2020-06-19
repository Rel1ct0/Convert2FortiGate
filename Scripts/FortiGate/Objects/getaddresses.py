def getaddresses(DATA: dict):
    for interface, iface_params in DATA.get('interfaces').items():  # Check all interfaces
        if acl := iface_params.get('acl-in'):  # Check applied ACLs
            for ace in DATA['acls'][acl]:
                if ace.get('dst') and ace['dst'].get('ip'):
                    if ace['dst']['ip'] == 'any':
                        ace['dst'] = 'any'
                    else:  # Not any
                        name = str()
                        if ace['dst']['mask'] == '255.255.255.255':
                            name = name + 'Host_'
                        else:
                            name = name + 'Net_'
                        name = name + ace['dst']['ip'] + '_' + ace['dst']['mask']
                        if not DATA['objects']['address'].get(name):  # This object does not exist, create it
                            DATA['objects']['address'][name] = dict()
                            DATA['objects']['address'][name]['prefix'] = ace['dst']['ip']
                            DATA['objects']['address'][name]['mask'] = ace['dst']['mask']
                if ace.get('src') and ace['src'].get('ip'):
                    if ace['src']['ip'] == 'any':
                        ace['src'] = 'any'
                    else:  # Not any
                        name = str()
                        if ace['src']['mask'] == '255.255.255.255':
                            name = name + 'Host_'
                        else:
                            name = name + 'Net_'
                        name = name + ace['src']['ip'] + '_' + ace['src']['mask']
                        if not DATA['objects']['address'].get(name):  # This object does not exist, create it
                            DATA['objects']['address'][name] = dict()
                            DATA['objects']['address'][name]['prefix'] = ace['src']['ip']
                            DATA['objects']['address'][name]['mask'] = ace['src']['mask']
    return