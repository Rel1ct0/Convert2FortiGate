import Scripts.FortiGate.Objects as Objects

def setobjects(DATA: dict) -> str:
    result = 'config firewall address\n'
    brk = ' '*4

    Objects.getaddresses(DATA)
    Objects.getservices(DATA)

    for object, params in DATA['objects']['address'].items():  # Writing address objects into config
        result = result + brk + 'edit ' + object + '\n'
        result = result + brk*2 + 'set subnet ' + params['prefix'] + ' ' + params['mask'] + '\n'
        if params.get('description'):
            result = result + brk * 2 + 'set comment "' + params['description'] + '"\n'
        result = result + brk + 'next\n'

    print('Objects converted')
    result = result + 'end\n'
    return result
