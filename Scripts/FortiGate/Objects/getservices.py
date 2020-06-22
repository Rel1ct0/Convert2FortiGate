def getservice(proto: str):
    protomatch = {'icmp': '1', 'igmp': '2', 'ipinip': '4', 'tcp': '6', 'udp': '17', 'gre': '47',
                  'esp': '50', 'ahp': '51', 'eigrp': '88', 'ospf': '89', 'nos': '94', 'pim': '103',
                  'pcp': '108'}
    if not proto.isdigit():
        return protomatch[proto]
    return proto

def getservices(DATA: dict) -> None:
    for interface, iface_params in DATA.get('interfaces').items():  # Check all interfaces
        if acl := iface_params.get('acl-in'):  # Check applied ACLs
            for ace in DATA['acls'][acl]:
                if not ace.get('service'):
                    continue
                if ace['service']['proto'] == 'ip':  # Nothing to do here
                    continue
                if ace['service']['proto'] in ['tcp', 'udp']:
                    srcportstart = ''
                    srcportend = ''
                    dstportstart = '1'
                    dstportend = '65535'
                    name = ace['service']['proto'].upper() + '_'
                    if ace['service'].get('dstport_compare'):
                        if ace['service']['dstport_compare'] == 'lt':
                            name = name + '1-'
                            dstportend = ace['service']['dstport']
                        name = name + ace['service']['dstport']
                        if ace['service']['dstport_compare'] == 'eq':
                            dstportstart = ace['service']['dstport']
                            dstportend = ace['service']['dstport']
                        if ace['service']['dstport_compare'] == 'ge':
                            name = name + '-65535'
                            dstportstart = ace['service']['dstport']
                        if ace['service']['dstport_compare'] == 'range':
                            name = name + '-' + ace['service']['dstport_end']
                            dstportstart = ace['service']['dstport']
                            dstportend = ace['service']['dstport_end']
                    if ace['service'].get('srcport_compare'):
                        if ace['service'].get('dstport_compare'):  # Beautiful underscore, not a mistake
                            name = name + '_'
                        name = name + 'SRC_'
                        if ace['service']['srcport_compare'] == 'eq':
                            srcportstart = ace['service']['srcport']
                            srcportend = ace['service']['srcport']
                        if ace['service']['srcport_compare'] == 'lt':
                            name = name + '1-'
                            srcportstart = '1'
                            srcportend = ace['service']['srcport']
                        name = name + ace['service']['srcport']
                        if ace['service']['srcport_compare'] == 'ge':
                            name = name + '-65535'
                            srcportstart = ace['service']['srcport']
                            srcportend = '65535'
                        if ace['service']['srcport_compare'] == 'range':
                            name = name + '-' + ace['service']['srcport_end']
                            srcportstart = ace['service']['srcport']
                            srcportend = ace['service']['srcport_end']
                    if not DATA['objects']['service'].get(name):  # Service does not exist, create it
                        print('Service', name, 'does not exist, creating')
                        DATA['objects']['service'][name] = dict()
                        DATA['objects']['service'][name]['proto'] = ace['service']['proto']
                        ports = srcportstart
                        if srcportend:
                            ports = ports + '-' + srcportend + ':'
                        ports = ports + dstportstart + '-' + dstportend
                        DATA['objects']['service'][name]['ports'] = ports
                else:
                    name = 'Proto_' + ace['service']['proto']
                    if not DATA['objects']['service'].get(name):
                        print('Service', name.upper(), 'does not exist, creating')
                    DATA['objects']['service'][name.upper()] = dict()
                    DATA['objects']['service'][name.upper()]['proto'] = getservice(ace['service']['proto'])
    return
