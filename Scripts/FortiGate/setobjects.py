def setobjects(DATA: dict) -> str:
    result = 'config firewall address\n'
    brk = ' '*4

    for interface, iface_params in DATA.get('interfaces').items():  # Check all interfaces
        if acl := iface_params.get('acl-in'):  # Check applied ACLs
            for ace in DATA['acls'][acl]:
                if ace.get('dst') and ace['dst'].get('ip'):
                    if ace['dst']['ip'] == 'any':
                        ace['dst'] = 'any'
                    else:
                        name = str()
                        if ace['dst']['mask'] == '255.255.255.255':
                            name = name + 'Host_'
                        else:
                            name = name + 'Net_'
                        name = name + ace['dst']['ip'] + '_' + ace['dst']['mask']
                        if not DATA['objects'].get(name):  # This object does not exist, create it
                            DATA['objects'][name] = dict()
                            DATA['objects'][name]['prefix'] = ace['dst']['ip']
                            DATA['objects'][name]['mask'] = ace['dst']['mask']

    for object, params in DATA['objects'].items():
        result = result + brk + 'edit ' + object + '\n'
        result = result + brk*2 + 'set subnet ' + params['prefix'] + ' ' + params['mask'] + '\n'
        if params.get('description'):
            result = result + brk * 2 + 'set comment "' + params['description'] + '"\n'
        result = result + brk + 'next\n'

    print('Objects converted')
    result = result + 'end\n'
    return result
