def setfirewallpolicy(DATA: dict) -> str:
    result = 'config firewall policy\n'
    brk = ' ' * 4
    for interface, iface_params in DATA.get('interfaces').items():
        if not DATA['interface_map'].get(interface):  # Skipped interface, ignore
            continue
        if acl := iface_params.get('acl-in'):  # This interface has ACL applied
            rule_counter = 1
            comment = str()
            for ace in DATA['acls'][acl]:  # Next ACE
                if ace.get('comments'):  # This ACE is a comment
                    comment = ace.get('comments')
                    continue
                result = result + brk + 'edit ' + acl + '_' + str(rule_counter) + '\n'
                if comment:  # Last ACE was a comment? Append it
                    result = result + brk*2 + 'set comments "' + comment.strip('"') + '"\n'
                    comment = str()
                result = result + brk * 2 + 'set srcintf ' + DATA['interface_map'][interface] + '\n'
                result = result + brk * 2 + 'set dstintf any\n'
                if ace['action'] == 'allow':
                    result = result + brk * 2 + 'set action accept\n'
               # result = result + brk * 2 + 'set service ' + ace['service']['object'] + '\n'
                result = result + brk + 'next\n'
                rule_counter += 1
        else:  # Interface does not have ACL applied
            result = result + brk + 'edit ' + DATA['interface_map'][interface] + '\n'
            result = result + brk * 2 + 'set srcintf ' + DATA['interface_map'][interface] + '\n'
            result = result + brk * 2 + 'set dstintf any\n'
            result = result + brk * 2 + 'set action accept\n'
            result = result + brk * 2 + 'set service ALL\n'
            result = result + brk * 2 + 'set srcaddr all\n'
            result = result + brk * 2 + 'set dstaddr all\n'
            result = result + brk + 'next\n'
    result = result + 'end\n'
    return result
