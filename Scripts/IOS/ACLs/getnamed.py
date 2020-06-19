import json

def getport(port: str):
    portmatch = {'bgp': '179', 'chargen': '19', 'cmd': '514', 'daytime': '13', 'discard': '9', 'domain': '53',
                 'echo': '7', 'exec': '512', 'finger': '79', 'ftp': '21', 'ftp-data': '20', 'gopher': '70',
                 'hostname': '101', 'ident': '113', 'irc': '194', 'klogin': '543', 'kshell': '544', 'login': '513',
                 'lpd': '515', 'msrpc': '135', 'nntp': '119', 'onep-plain': '15001', 'onep-tls': '15002',
                 'pim-auto-rp': '496', 'pop2': '109', 'pop3': '110', 'smtp': '25', 'sunrpc': '111', 'tacacs': '49',
                 'talk': '517', 'telnet': '23', 'uucp': '540', 'whois': '43', 'www': '80', 'biff': '512',
                 'bootpc': '68', 'bootps': '67', 'dnsix': '195', 'isakmp': '500', 'mobile-ip': '434',
                 'nameserver': '42', 'netbios-dgm': '138', 'netbios-ns': '137', 'netbios-ss': '139',
                 'non500-isakmp': '4500', 'ntp': '123', 'rip': '520', 'ripv6': '521', 'snmp': '161',
                 'snmptrap': '162', 'syslog': '514', 'tftp': '69', 'time': '37', 'who': '513', 'xdmcp': '177'}
    if not port.isdigit():
        return portmatch[port]
    return port


def getnamed(DATA) -> dict:
    result = dict()
    StdACL_detected = False
    ExtACL_detected = False
    ACLName = ''
    ACL = list()
    for _ in DATA:
        data = _.strip().split()
        if len(data) == 0:
            continue
        if data[0] == "ip" and data[1] == "access-list":
            if StdACL_detected or ExtACL_detected:  # New ACL detected, save previous one
                StdACL_detected = False
                ExtACL_detected = False
                result[ACLName] = ACL
                ACLName = ''
                ACL = list()
            if data[2] == "standard":
                StdACL_detected = True
                ACLName = data[3]
            elif data[2] == "extended":
                ExtACL_detected = True
                ACLName = data[3]
            continue
        if StdACL_detected:
            if data[0] in ['permit', 'deny', 'remark']:
                ACE = dict()
                if data[0] == 'remark':
                    ACE['comments'] = '"' + ' '.join(map(str, data[1:])) + '"'
                else:  # Permit or deny
                    ACE['src'] = dict()
                    if data[0] == 'permit':
                        ACE['action'] = 'allow'
                    else:
                        ACE['action'] = 'deny'
                    if data[1] == 'any':
                        ACE['src']['ip'] = 'any'
                    elif data[1] == 'host':
                        ACE['src']['ip'] = data[2]
                        ACE['src']['mask'] = '255.255.255.255'
                    else:
                        ACE['src']['ip'] = data[1]
                        if len(data) == 3:  # Wildcard mask defined
                            wildmask = data[2].split('.')
                            mask = [str(255 - int(x)) for x in wildmask]
                            ACE['src']['mask'] = '.'.join(mask)
                        else:  # Wildcard mask not defined
                            ACE['src']['mask'] = '255.255.255.255'
                    ACE['dst'] = dict()
                    ACE['dst']['ip'] = 'any'
                    ACE['service'] = dict()
                    ACE['service']['proto'] = 'ip'
                ACL.append(ACE)
            else:
                StdACL_detected = False
                result[ACLName] = ACL
                ACLName = ''
                ACL = list()
        if ExtACL_detected:
            if data[0] in ['permit', 'deny', 'remark']:
                ACE = dict()
                if data[0] == 'remark':
                    ACE['comments'] = '"' + ' '.join(map(str, data[1:])) + '"'
                elif data[0] in ['permit', 'deny']:  # Must be permit or deny ACE
                    if data[0] == 'permit':
                        ACE['action'] = 'allow'
                    else:
                        ACE['action'] = 'deny'
                    ACE['service'] = dict()
                    ACE['service']['proto'] = data[1]
                    ACE['src'] = dict()
                    if data[2] == 'any':  # Source
                        ACE['src']['ip'] = 'any'
                        data = data[3:]  # Cut off src
                    elif data[2] == 'host':
                        ACE['src']['ip'] = data[3]
                        ACE['src']['mask'] = '255.255.255.255'
                        data = data[4:]  # Cut off src
                    elif data[2] == 'object-group':
                        ACE['src']['object'] = data[3]
                        data = data[4:]  # Cut off src
                    else:
                        ACE['src']['ip'] = data[2]
                        wildmask = data[3].split('.')
                        mask = [str(255 - int(x)) for x in wildmask]
                        ACE['src']['mask'] = '.'.join(mask)
                        data = data[4:]  # Cut off src
                    if data[0] in ['eq', 'gt', 'lt', 'neq']:  # Is source port defined?
                        ACE['service']['srcport'] = getport(data[1])
                        ACE['service']['srcport_compare'] = data[0]
                        data = data[2:]
                    elif data[0] == 'range':
                        ACE['service']['srcport'] = getport(data[1])
                        ACE['service']['srcport_end'] = getport(data[2])
                        ACE['service']['srcport_compare'] = data[0]
                        data = data[3:]
                    ACE['dst'] = dict()
                    if data[0] == 'any':  # Destination
                        ACE['dst']['ip'] = 'any'
                        data = data[1:]  # Cut off src
                    elif data[0] == 'host':
                        ACE['dst']['ip'] = data[1]
                        ACE['dst']['mask'] = '255.255.255.255'
                        data = data[2:]  # Cut off src
                    elif data[0] == 'object-group':
                        ACE['dst']['object'] = data[1]
                        data = data[2:]  # Cut off src
                    else:
                        ACE['dst']['ip'] = data[0]
                        wildmask = data[1].split('.')
                        mask = [str(255 - int(x)) for x in wildmask]
                        ACE['dst']['mask'] = '.'.join(mask)
                        data = data[2:]  # Cut off src
                    if data:  # Dst port can be absent
                        if data[0] in ['eq', 'gt', 'lt', 'neq']:
                            ACE['service']['dstport'] = getport(data[1])
                            ACE['service']['dstport_compare'] = data[0]
                        elif data[0] == 'range':
                            ACE['service']['dstport'] = getport(data[1])
                            ACE['service']['dstport_end'] = getport(data[2])
                            ACE['service']['dstport_compare'] = data[0]
                ACL.append(ACE)
            else:
                ExtACL_detected = False
                result[ACLName] = ACL
                ACLName = ''
                ACL = list()
    return result
