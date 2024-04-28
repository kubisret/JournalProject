import random


def create_default_identifier():
    set_symbol = list('0123456789')
    result_identifier = ''.join(random.sample(set_symbol, 10))
    return result_identifier


def create_default_key():
    set_symbol = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789')
    result_key = ''.join(random.sample(set_symbol, 15))
    return result_key
