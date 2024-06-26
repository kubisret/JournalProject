import re


def check_validate_password(password):
    # Проверяем длину пароля
    if len(password) < 8 or len(password) > 128:
        return False, 'Слишком маленькая длина пароля.'

    # Проверяем наличие строчной буквы
    if not re.search("[a-z]", password):
        return False, 'Необходимо наличие одной или более строчных букв.'

    # Проверяем наличие цифры
    if not re.search("[0-9]", password):
        return False, 'Пароль должен содержать одну или более цифр.'

    ############################## FOR ADDED RELIABILITY ##############################
    # Проверяем наличие русских букв
    # if re.search("[а-яА-Я]", password):
    #     return False, 'В пароле могут использоваться только буквы латинского алфавита.'

    # Проверяем наличие заглавной буквы
    # if not re.search("[A-Z]", password):
    #     return False, 'Необходимо наличие одной или более заглавных букв.'

    # Проверяем наличие специального символа
    # if re.search("[/@?#<>%&;:+_[]{}|]", password):
    #     return False, 'В пароле используются недопустимые символы из списка: /@?#<>%&;:+_[]{}|.'
    ###################################################################################

    return True, 'Надежный пароль'


def check_validate_identifier(list_identifier):
    response = all([False if not symbol.isdigit() else True for symbol in list_identifier])
    return response

