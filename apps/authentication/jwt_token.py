# Modulos de django
from django.conf import settings

# Modulos de JWT
import jwt

# Modulos locales
from .timezone import get_timedelta, get_timezone


def generate_jwt_token(email, username, token, days=0, minutes=0):
    access_token = jwt.encode({
        'email': email,
        'username': username,
        'type_token': 'Bearer',
        'token': token,
        'exp': get_timedelta(days=days, minutes=minutes),
        'iat': get_timezone(),
    }, settings.SECRET_KEY, algorithm='HS256')

    return access_token.decode('utf-8')
