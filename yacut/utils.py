from random import choice

from settings import ALLOWED_SYMBOLS_FOR_CUSTOM_ID, LINK_IDENTIFIER_MAX_LENGTH


def check_custom_id(custom_id):
    'Проверка идентификатора на соответствие требованиям'
    if len(custom_id) > LINK_IDENTIFIER_MAX_LENGTH:
        return False
    for symbol in custom_id:
        if symbol not in ALLOWED_SYMBOLS_FOR_CUSTOM_ID:
            return False
    return True


def get_unique_short_id():
    'Генерирует случайную последовательность из 6 символов'
    return ''.join(choice(ALLOWED_SYMBOLS_FOR_CUSTOM_ID) for _ in range(6))
