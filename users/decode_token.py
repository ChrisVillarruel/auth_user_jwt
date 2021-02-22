# users.decode_token

from datetime import datetime, timedelta
from django.conf import settings
import jwt


try:
    # Creamos el metodo get_date que me retornara la fecha de expiración
    # del token actual
    def get_token_expiration_date(token):
        payload = jwt.decode(token, settings.SECRET_KEY)
        timestamp = payload['exp']
        dt_object = datetime.fromtimestamp(timestamp)

        return dt_object.strftime('%d-%b-%y')


except jwt.ExpiredSignatureError as e:
    msg = 'Su sesión actual ya expiro. Vuelva a iniciar sesión para continuar.'
    raise exceptions.AuthenticationFailed(msg)
except jwt.exceptions.DecodeError as e:
    msg = 'Autenticación no válida. No se pudo decodificar el token.'
    raise exceptions.AuthenticationFailed(msg)
