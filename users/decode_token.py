# users.decode_token

from rest_framework import exceptions
from datetime import datetime, timedelta
from django.conf import settings
import jwt


# Creamos el metodo get_date que me retornara la fecha de expiración del token actual
def get_token_expiration_date(token):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        # De la fecha de expiración del token le restamos
        # cinco dias, para que se actualice el token antes
        # de la fecha de expiración.
        timestamp = payload['exp'] - 432000
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object.strftime('%d-%b-%y')

    except jwt.ExpiredSignatureError as e:
        msg = 'Su sesión actual ya caduco. Intente Iniciar sesión nuevamente. Si persiste el error comuniquese con el administrador del sistema.'
        raise exceptions.AuthenticationFailed(msg)
    except jwt.exceptions.DecodeError as e:
        msg = 'Autenticación no válida. No se pudo decodificar el token.'
        raise exceptions.AuthenticationFailed(msg)
