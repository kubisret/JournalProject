
def create_default_identifier():
    set_symbol = set('0123456789')
    result_identifier = ''.join(list(set_symbol))
    return result_identifier


def create_default_key():
    set_symbol = set('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789')
    result_key = ''.join(list(set_symbol)[:15])
    return result_key
