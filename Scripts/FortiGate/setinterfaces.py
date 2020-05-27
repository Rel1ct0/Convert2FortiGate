def setinterfaces(DATA: dict) -> str:
    result = 'config system interface\n'
    brk = ' '*4
    next_phys_port_number = 1
    interface_map = dict()
    for interface, params in DATA['interfaces'].items():
        if params['type'] == 'tunnel':  #ignore tunnel interfaces
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
            result = result + brk*2 + 'set ip ' + params['ip'] + ' ' + params['netmask'] + '\n'
        if params['shutdown']:
            result = result + brk * 2 + 'set status down\n'
        result = result + brk + 'next\n'
    print('Interfaces converted')
    result = result + 'end\n'
    DATA['interface_map'] = interface_map
    return result
