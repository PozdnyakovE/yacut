import os
import string


ORIGINAL_LINK_MAX_LENGTH = 256
SHORT_LINK_MAX_LENGTH = 128
LINK_IDENTIFIER_MAX_LENGTH = 16
HOST_ADDRESS = 'http://localhost/'

ALLOWED_SYMBOLS_FOR_CUSTOM_ID = (string.ascii_lowercase +
                                 string.ascii_uppercase + string.digits)
URL_PATTERN = ('^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]'
               '{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()'
               '@:%_\\+.~#?&\\/=]*)$')


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
