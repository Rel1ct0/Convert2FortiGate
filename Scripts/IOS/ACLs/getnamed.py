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
            if StdACL_detected or ExtACL_detected:
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
                    ACE['proto'] = 'ip'
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
                    ACE['proto'] = data[1]
                    ACE['src'] = dict()
                    if data[2] == 'any':  # Source
                        ACE['src']['ip'] = 'any'
                        data = data[3:]  # Cut off src
                    elif data[2] == 'host':
                        ACE['src']['ip'] = data[3]
                        ACE['src']['mask'] = '255.255.255.255'
                        data = data[4:]  # Cut off src
                    elif data[2] == 'object-group':
                        ACE['src']['ogroup'] = data[3]
                        data = data[4:]  # Cut off src
                    else:
                        ACE['src']['ip'] = data[2]
                        wildmask = data[3].split('.')
                        mask = [str(255 - int(x)) for x in wildmask]
                        ACE['src']['mask'] = '.'.join(mask)
                        data = data[4:]  # Cut off src
                    if data[0] in ['eq', 'gt', 'lt', 'neq']:  # Is source port defined?
                        ACE['src']['srcport'] = data[1]
                        ACE['src']['srcport_compare'] = data[0]
                        data = data[2:]
                    elif data[0] == 'range':
                        ACE['src']['srcport'] = data[1]
                        ACE['src']['srcport_end'] = data[2]
                        ACE['src']['port_compare'] = data[0]
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
                        ACE['dst']['ogroup'] = data[1]
                        data = data[2:]  # Cut off src
                    else:
                        ACE['dst']['ip'] = data[0]
                        wildmask = data[1].split('.')
                        mask = [str(255 - int(x)) for x in wildmask]
                        ACE['dst']['mask'] = '.'.join(mask)
                        data = data[2:]  # Cut off src
                    if data:  # Dst port can be absent
                        if data[0] in ['eq', 'gt', 'lt', 'neq']:
                            ACE['dst']['dstport'] = data[1]
                            ACE['dst']['dstport_compare'] = data[0]
                        elif data[0] == 'range':
                            ACE['dst']['dstport'] = data[1]
                            ACE['dst']['dstport_end'] = data[2]
                            ACE['dst']['dstport_compare'] = data[0]
                ACL.append(ACE)
            else:
                ExtACL_detected = False
                result[ACLName] = ACL
                ACLName = ''
                ACL = list()
    return result
