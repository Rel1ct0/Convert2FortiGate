def setzones(DATA: dict) -> str:
    result = 'config system zone\n'
    brk = ' ' * 4
    for zone, members in DATA['zones'].items():
        real_members = list()
        for member in members:  # Does a zone have any members? Lets map them to real port names
            if DATA['interface_map'].get(member):
                real_members.append(DATA['interface_map'][member])
        if real_members:  # Do not create a zone with no members
            result = result + brk + 'edit ' + zone + '\n'
            result = result + brk * 2 + 'set members ' + ' '.join(map(str, real_members)) + '\n'
            result = result + brk + 'next\n'
            result = result + 'end\n'
    return result
