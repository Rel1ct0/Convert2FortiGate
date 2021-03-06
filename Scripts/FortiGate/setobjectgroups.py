def setobjectgroups(DATA: dict) -> str:
    result = 'config firewall addrgrp\n'
    brk = ' ' * 4
    if not DATA.get('objects'):
        DATA['objects'] = dict()
        DATA['objects']['address'] = dict()
        DATA['objects']['service'] = dict()
    if not DATA.get('object-groups'):
        return ''
    for ogroup in DATA['object-groups']:
        result = result + brk + 'edit ' + ogroup['name'] + '\n'
        if ogroup.get('description'):
            result = result + brk * 2 + 'set comment "' + ogroup['description'] + '"\n'
        members = str()
        for member in ogroup.get('items'):
            if member[0] == 'group-object':  # add child o-group to list of members
                members = members + ' "' + member[1] + '"'
            if member[0] == 'host':  # add child object to list of members
                object_name = 'Host_' + member[1]
                if not DATA['objects']['address'].get(object_name):  # object defined in object group, we must create it
                    DATA['objects']['address'][object_name] = dict()
                    DATA['objects']['address'][object_name]['type'] = 'subnet'
                    DATA['objects']['address'][object_name]['prefix'] = member[1]
                    DATA['objects']['address'][object_name]['mask'] = '255.255.255.255'
                members = members + ' "' + object_name + '"'
            if member[0] == 'network':  # add child object to list of members
                object_name = 'Net_' + member[1] + '_' + member[2]
                if not DATA['objects']['address'].get(object_name):  # object defined in object group, we must create it
                    DATA['objects']['address'][object_name] = dict()
                    DATA['objects']['address'][object_name]['type'] = 'subnet'
                    DATA['objects']['address'][object_name]['prefix'] = member[1]
                    DATA['objects']['address'][object_name]['mask'] = member[2]
                members = members + ' "' + object_name + '"'
        if members:
            result = result + brk * 2 + 'set member' + members + "\n"
        result = result + brk + 'next\n'
    print('Object groups converted')
    result = result + 'end\n'
    return result
