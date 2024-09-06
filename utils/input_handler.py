def int_handler(message):
    input_num = input(message)

    try:
        input_num = int(input_num)
        if input_num <= 0:
            input_num = -1
    except ValueError:
        print('Invalid positive integer input !')
        input_num = -1
    finally:
        return input_num
