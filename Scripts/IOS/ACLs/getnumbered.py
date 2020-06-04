def getnumbered(DATA) -> dict:
    result = dict()
    for _ in DATA:
        data = _.strip().split()
        if len(data) == 0:
            continue
        if data[0] == "access-list":
            if data[1].isdigit():
                if int(data[1]) < 100 or (1300 <= int(data[1]) < 2000):  # Standard ACL
                    if not result.get(data[1]):  # First line of ACL, create it
                        result[data[1]] = list()
                    ACE = dict()
                    if data[2] == 'remark':
                        ACE['comments'] = '"' + ' '.join(map(str, data[3:])) + '"'
                    else:  # Permit or deny
                        ACE['src'] = dict()
                        if data[2] == 'permit':
                            ACE['action'] = 'allow'
                        else:
                            ACE['action'] = 'deny'
                        if data[3] == 'any':
                            ACE['src']['ip'] = 'any'
                        elif data[3] == 'host':
                            ACE['src']['ip'] = data[4]
                            ACE['src']['mask'] = '255.255.255.255'
                        else:
                            ACE['src']['ip'] = data[3]
                            if len(data) == 5:  # Wildcard mask defined
                                wildmask = data[4].split('.')
                                mask = [str(255 - int(x)) for x in wildmask]
                                ACE['src']['mask'] = '.'.join(mask)
                            else:  # Wildcard mask not defined
                                ACE['src']['mask'] = '255.255.255.255'
                        ACE['dst'] = dict()
                        ACE['dst']['ip'] = 'any'
                        ACE['proto'] = 'ip'
                    result[data[1]].append(ACE)
                if (100 <= int(data[1]) < 200) or (2000 <= int(data[1]) < 2700):  # Extended ACL
                    ACLName = data[1]
                    if not result.get(ACLName):  # First line of ACL, create it
                        result[ACLName] = list()
                    ACE = dict()
                    if data[2] == 'remark':
                        ACE['comments'] = '"' + ' '.join(map(str, data[3:])) + '"'
                    elif data[2] != 'dynamic':  # Must be permit or deny ACE
                        if data[2] == 'permit':
                            ACE['action'] = 'allow'
                        else:
                            ACE['action'] = 'deny'
                        ACE['proto'] = data[3]
                        ACE['src'] = dict()
                        if data[4] == 'any':  # Source
                            ACE['src']['ip'] = 'any'
                            data = data[5:]  # Cut off src
                        elif data[4] == 'host':
                            ACE['src']['ip'] = data[5]
                            ACE['src']['mask'] = '255.255.255.255'
                            data = data[5:]  # Cut off src
                        else:
                            ACE['src']['ip'] = data[4]
                            wildmask = data[5].split('.')
                            mask = [str(255 - int(x)) for x in wildmask]
                            ACE['src']['mask'] = '.'.join(mask)
                            data = data[6:]  # Cut off src
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
                            data = data[3:]  # Cut off src
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
                    result[ACLName].append(ACE)
    return result
