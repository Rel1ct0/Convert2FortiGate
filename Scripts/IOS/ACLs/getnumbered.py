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
                        if data[2] == 'permit':
                            ACE['action'] = 'allow'
                        else:
                            ACE['action'] = 'deny'
                        if data[3] == 'any':
                            ACE['srcip'] = 'any'
                        elif data[3] == 'host':
                            ACE['srcip'] = data[4]
                            ACE['srcmask'] = '255.255.255.255'
                        else:
                            ACE['srcip'] = data[3]
                            if len(data) == 5:  # Wildcard mask defined
                                wildmask = data[4].split('.')
                                mask = [str(255 - int(x)) for x in wildmask]
                                ACE['srcmask'] = '.'.join(mask)
                            else:  # Wildcard mask not defined
                                ACE['srcmask'] = '255.255.255.255'
                        ACE['dstip'] = 'any'
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
                        if data[4] == 'any':  # Source
                            ACE['srcip'] = 'any'
                            data = data[5:]  # Cut off src
                        elif data[4] == 'host':
                            ACE['srcip'] = data[5]
                            ACE['srcmask'] = '255.255.255.255'
                            data = data[5:]  # Cut off src
                        else:
                            ACE['srcip'] = data[4]
                            wildmask = data[5].split('.')
                            mask = [str(255 - int(x)) for x in wildmask]
                            ACE['srcmask'] = '.'.join(mask)
                            data = data[6:]  # Cut off src
                        if data[0] in ['eq', 'gt', 'lt', 'neq']:  # Is source port defined?
                            ACE['srcport'] = data[1]
                            ACE['srcport_compare'] = data[0]
                            data = data[2:]
                        elif data[0] == 'range':
                            ACE['srcport'] = data[1]
                            ACE['srcport_end'] = data[2]
                            ACE['srcport_compare'] = data[0]
                            data = data[3:]
                        if data[0] == 'any':  # Destination
                            ACE['dstip'] = 'any'
                            data = data[1:]  # Cut off src
                        elif data[0] == 'host':
                            ACE['dstip'] = data[1]
                            ACE['dstmask'] = '255.255.255.255'
                            data = data[3:]  # Cut off src
                        else:
                            ACE['dstip'] = data[0]
                            wildmask = data[1].split('.')
                            mask = [str(255 - int(x)) for x in wildmask]
                            ACE['dstmask'] = '.'.join(mask)
                            data = data[2:]  # Cut off src
                        if data:  # Dst port can be absent
                            if data[0] in ['eq', 'gt', 'lt', 'neq']:
                                ACE['dstport'] = data[1]
                                ACE['dstport_compare'] = data[0]
                            elif data[0] == 'range':
                                ACE['dstport'] = data[1]
                                ACE['dstport_end'] = data[2]
                                ACE['dstport_compare'] = data[0]
                    result[ACLName].append(ACE)
    return result
