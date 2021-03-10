# Modulo de rest_framework
from rest_framework import serializers

# Modulos de django
from django.conf import settings

# Modulo de jwt
import jwt

# Modulo local
from apps.users.models import User


class LogoutSerializer(serializers.ModelSerializer):
    """
    Esta clase permitira cerrar su 'sesión' y de manera interna actualizar
    los tokens almacenados, de esa forma evitamos que un usuario
    le pertenezcan multiples tokens.


    """
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ['refresh_token', 'access_token', 'token']

    def validate(self, attrs):
        """
        Obtenemos el token.
        Puede ser el token de acceso o de actualización


        """
        token = attrs.get('token', None)
        try:
            """
            Decodificamos el token y obtenemos el usuario atravez
            de su dirección de correo.

            Una vez obtenido el usuario, al token de acceso y al token
            de actualización lo asignamos como vacio
            y llamamos al metodo save para que se encarge de generar
            un nuevo token


            """

            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(email=payload['email'])
            user.refresh_token = None
            user.access_token = None
            user.save()

        except jwt.exceptions.DecodeError as e:
            msg = 'Error al decodificar el token.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError as e:
            msg = 'Su sesión actual ya expiro. Vuelva a iniciar sesión para continuar.'
            raise exceptions.AuthenticationFailed(msg)

        return attrs
