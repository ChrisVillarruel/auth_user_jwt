import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """
        El método `authenticate` se llama en cada solicitud independientemente de
        si el punto final requiere autenticación.

        `authenticate` tiene dos posibles valores de retorno:

        1) "Ninguno":   devolvemos "Ninguno" si no deseamos autenticarnos. Generalmente
                        esto significa que sabemos que la autenticación fallará. Un ejemplo de
                        esto es cuando la solicitud no incluye un token en el
                        encabezados.

        2) `(usuario, token)` - Devolvemos una combinación de usuario / token cuando
                    la autenticación es exitosa.

                    Si no se cumple ninguno de los casos, significa que hay un error
                    y no devolvemos nada. Simplemente elevamos el `AuthenticationFailed`
                    excepción y deje que Django REST Framework manejar el resto.

        """
        request.user = None

        # `auth_header` debe ser una matriz con dos elementos:
        # 1) el nombre de el encabezado de autenticación (en este caso, "Bearer") y
        # 2) el JWT contra el que debemos autenticarnos.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Encabezado de token no válido. No se proporcionaron credenciales.
            # No intente autenticarse.
            return None

        elif len(auth_header) > 2:
            # Encabezado de token no válido. La cadena Token no debe contener espacios.
            # No intente autenticarse.
            return None

        # La biblioteca JWT que estamos usando no puede manejar el tipo `byte`, que es
        # comúnmente utilizado por las bibliotecas estándar en Python 3. Para solucionar esto,
        # simplemente tenemos que decodificar `prefix` y` token`. Esto no hace para nada
        # código limpio, pero es una buena decisión porque obtendríamos un error
        # si no decodificamos estos valores.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # El prefijo de encabezado de autenticación no es el que esperábamos.
            # No intente autenticarse.
            return None

        # A estas alturas, estamos seguros de que existe una * posibilidad *
        # de que la autenticación puede tener éxito. Delegamos la autenticación
        # de credenciales real al método a continuación.
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """

        Intente autenticar las credenciales proporcionadas.
        Si la autenticación es exitosa, devuelva el usuario y el token.
        Si no, arroja un error.

        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except jwt.ExpiredSignatureError as e:
            msg = 'Su sesión actual ya expiro'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.exceptions.DecodeError as e:
            msg = 'Autenticación no válida. No se pudo decodificar el token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No se encontró ningún usuario que coincida con este token.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Este usuario ha sido desactivado.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
