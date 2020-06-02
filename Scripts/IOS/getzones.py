def getzones(DATA) -> dict:  # getting 'interfaces' dict as input
    result = dict()
    for interface, params in DATA.items():
        if params.get('zone'):
            if not result.get(params['zone']):
                result[params['zone']] = list()
            result[params['zone']].append(interface)
    return result
