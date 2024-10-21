from business_layer.authentication import Authentication


def int_handler(message):
    input_num = input(message)

    try:
        input_num = int(input_num)
        if input_num <= 0 or not isinstance(input_num, int):
            input_num = -1
    except ValueError:
        print('Invalid positive integer input !')
        input_num = -1
    finally:
        return input_num


def string_handler(message):
    input_str = input(message)
    if not input_str.isalpha():
        return ''
    return input_str


def username_handler(message):
    input_username = input(message)
    if not Authentication.check_username_format(input_username):
        return ''
    return input_username


def password_handler(message):
    input_password = input(message)
    if not Authentication.check_password_format(input_password):
        return ''
    return input_password
