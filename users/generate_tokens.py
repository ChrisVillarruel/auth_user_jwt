from datetime import datetime, timedelta
from django.conf import settings
import datetime
import pytz
import jwt


def generate_jwt_access_token(email, username):
    """
    Generar un token de acceso JWT que almacena información del usuario que se registro y tiene
    un tiempo de vida muy reducida. Este tipo de token es utilizado para la activación
    de una cuenta. Su tiempo de vida va entre los cinco minutos y a un dia
    """
    exp = datetime.datetime.now(tz=pytz.timezone('America/Mexico_City')) + datetime.timedelta(days=1)

    access_token = jwt.encode({
        'email': email,
        'username': username,
        'token_type': 'access',
        'exp': exp,
        'iat': datetime.datetime.now(tz=pytz.timezone('America/Mexico_City')),
    }, settings.SECRET_KEY, algorithm='HS256')

    return access_token.decode('utf-8')


def generate_jwt_refresh_token(email, username):
    """
    Generar un refresh_token de JWT que almacena información del usuario que se registro y tiene
    un tiempo vida mas alrgo. Este tipo de token es utilizado para la navegación dentro del sistema
    sin la necesidad de iniciar sesión cada media hora. Este tipo de token puede durar el tiempo
    que el desarrollador decida. En este caso duarara 150 dias.
    """

    exp = datetime.datetime.now(tz=pytz.timezone('America/Mexico_City')) + datetime.timedelta(days=10)

    refresh_token = jwt.encode({
        'email': email,
        'username': username,
        'token_type': 'refresh',
        'exp': exp,
        'iat': datetime.datetime.now(tz=pytz.timezone('America/Mexico_City')),
    }, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token.decode('utf-8')
