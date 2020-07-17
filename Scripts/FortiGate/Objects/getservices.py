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
            for counter in range(0, len(DATA['acls'][acl])):  # For every line in ACL
                if not DATA['acls'][acl][counter].get('service'):
                    DATA['acls'][acl][counter]['service'] = dict()
                    DATA['acls'][acl][counter]['service']['object'] = 'all'
                    continue
                if DATA['acls'][acl][counter]['service']['proto'] == 'ip':  # Nothing to do here
                    DATA['acls'][acl][counter]['service']['object'] = 'all'
                    continue
                if DATA['acls'][acl][counter]['service']['proto'] in ['tcp', 'udp']:
                    srcportstart = ''
                    srcportend = ''
                    dstportstart = '1'
                    dstportend = '65535'
                    name = DATA['acls'][acl][counter]['service']['proto'].upper()
                    if DATA['acls'][acl][counter]['service'].get('dstport_compare'):
                        if DATA['acls'][acl][counter]['service']['dstport_compare'] == 'lt':
                            name = name + '_1-'
                            dstportend = DATA['acls'][acl][counter]['service']['dstport']
                        name = name + '_' + DATA['acls'][acl][counter]['service']['dstport']
                        if DATA['acls'][acl][counter]['service']['dstport_compare'] == 'eq':
                            dstportstart = DATA['acls'][acl][counter]['service']['dstport']
                            dstportend = DATA['acls'][acl][counter]['service']['dstport']
                        if DATA['acls'][acl][counter]['service']['dstport_compare'] == 'ge':
                            name = name + '-65535'
                            dstportstart = DATA['acls'][acl][counter]['service']['dstport']
                        if DATA['acls'][acl][counter]['service']['dstport_compare'] == 'range':
                            name = name + '-' + DATA['acls'][acl][counter]['service']['dstport_end']
                            dstportstart = DATA['acls'][acl][counter]['service']['dstport']
                            dstportend = DATA['acls'][acl][counter]['service']['dstport_end']
                    if DATA['acls'][acl][counter]['service'].get('srcport_compare'):
                        name = name + '_SRC_'
                        if DATA['acls'][acl][counter]['service']['srcport_compare'] == 'eq':
                            srcportstart = DATA['acls'][acl][counter]['service']['srcport']
                            srcportend = DATA['acls'][acl][counter]['service']['srcport']
                        if DATA['acls'][acl][counter]['service']['srcport_compare'] == 'lt':
                            name = name + '1-'
                            srcportstart = '1'
                            srcportend = DATA['acls'][acl][counter]['service']['srcport']
                        name = name + DATA['acls'][acl][counter]['service']['srcport']
                        if DATA['acls'][acl][counter]['service']['srcport_compare'] == 'ge':
                            name = name + '-65535'
                            srcportstart = DATA['acls'][acl][counter]['service']['srcport']
                            srcportend = '65535'
                        if DATA['acls'][acl][counter]['service']['srcport_compare'] == 'range':
                            name = name + '-' + DATA['acls'][acl][counter]['service']['srcport_end']
                            srcportstart = DATA['acls'][acl][counter]['service']['srcport']
                            srcportend = DATA['acls'][acl][counter]['service']['srcport_end']
                    if not DATA['objects']['service'].get(name):  # Service does not exist, create it
                        # print('Service', name, 'does not exist, creating')
                        DATA['objects']['service'][name] = dict()
                        DATA['objects']['service'][name]['proto'] = DATA['acls'][acl][counter]['service']['proto']
                        ports = srcportstart
                        if srcportend:
                            ports = ports + '-' + srcportend + ':'
                        ports = ports + dstportstart + '-' + dstportend
                        DATA['objects']['service'][name]['ports'] = ports

                else:
                    name = 'PROTO_' + DATA['acls'][acl][counter]['service']['proto'].upper()
                    # if not DATA['objects']['service'].get(name):
                    #    print('Service', name, 'does not exist, creating')
                    DATA['objects']['service'][name] = dict()
                    DATA['objects']['service'][name]['proto'] = getservice(DATA['acls'][acl][counter]['service']['proto'])
                DATA['acls'][acl][counter]['service']['object'] = name
    return
