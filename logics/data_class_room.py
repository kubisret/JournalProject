
def create_default_identifier():
    set_symbol = set('01234567890')
    result_identifier = [''.join(list(set_symbol)[:4]),
                         ''.join(list(set_symbol)[:4]),
                         ''.join(list(set_symbol)[:4])]
    return ''.join(result_identifier)


def create_default_key():
    set_symbol = set('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789')
    result_key = ''.join(list(set_symbol)[:15])
    return result_key
