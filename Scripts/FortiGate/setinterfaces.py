def setinterfaces(DATA: dict) -> str:
    result = 'config system interface\n'
    brk = ' '*4  # Standard FortiGate indentation
    next_phys_port_number = 1  # Will number physical ports starting with port1
    interface_map = dict()  # Will save mapping between old and new interfaces to be used in other scripts
    for interface, params in DATA['interfaces'].items():
        if params['type'] == 'tunnel':  # ignore tunnel interfaces
            print('Skipping tunnel interface', interface)
            continue
        if params['type'] == 'physical' and params['shutdown'] and (not params.get('ip')):
            print('Skipping disabled interface', interface, 'with no ip address')
            continue
        if params['type'] == 'physical':
            result = result + brk + 'edit port' + str(next_phys_port_number) + '\n'
            interface_map[interface] = 'port' + str(next_phys_port_number)
            next_phys_port_number += 1
        if params['type'] == 'subinterface':
            interface_map[interface] = interface_map[params['parent']] + '_' + params['vlan']
            result = result + brk + 'edit ' + interface_map[params['parent']] + '_' + params['vlan'] + '\n'
            result = result + brk * 2 + 'set interface ' + interface_map[params['parent']] + '\n'
            result = result + brk * 2 + 'set vlanid ' + params['vlan'] + '\n'
        if params.get('ip'):
            result = result + brk * 2 + 'set ip ' + params['ip'] + ' ' + params['netmask'] + '\n'
        if params.get('description'):
            result = result + brk * 2 + 'set comment ' + params['description'] + '\n'
        if params['shutdown']:
            result = result + brk * 2 + 'set status down\n'
        if params.get('secondary'):
            result = result + brk * 2 + 'set secondary-ip enable\n'
            result = result + brk * 2 + 'config secondaryip\n'
            n = 1
            for nextIp in params['secondary']:
                result = result + brk * 3 + 'edit ' + str(n) + '\n'
                result = result + brk * 4 + 'set ip ' + nextIp[0] + ' ' + nextIp[1] + '\n'
                result = result + brk * 3 + 'next\n'
                n += 1
            result = result + brk * 2 + 'end\n'
        if params.get('dhcp-relay'):
            result = result + brk * 2 + 'set dhcp-relay-service enable\n'
            result = result + brk * 2 + 'set dhcp-relay-ip ' + ' '.join(map(str, params['dhcp-relay'])) + '\n'
        result = result + brk + 'next\n'
    print('Interfaces converted')
    result = result + 'end\n'
    DATA['interface_map'] = interface_map
    return result
