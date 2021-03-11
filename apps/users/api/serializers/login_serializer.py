#  Modulos de rest_framework
from rest_framework import serializers
from rest_framework import exceptions

# Modulos de django
from django.contrib.auth import authenticate

# Modulos locales
from apps.users.models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']
        read_only_fields = ('token',)

    def validate(self, data):
        """
        El método `validate` es donde nos aseguramos de que la
        instancia de `LoginSerializer` tiene todos los campos validados.
        Significa que ha proporcionado un correo electrónico y contraseña.
        y que esta combinación coincide con uno de los usuarios en nuestra base de datos.


        """
        email = data.get('email', None)
        password = data.get('password', None)

        """
        El método `authenticate` es proporcionado por Django y maneja la verificación
        para un usuario que coincide con esta combinación de correo electrónico y contraseña.
        Date cuenta cómo pasamos `email` como el valor de` username` ya que en nuestro User
        modelo establecemos `USERNAME_FIELD` como` email`.


        """
        user = authenticate(username=email, password=password)

        """
        Si no se encontró ningún usuario que coincida con esta combinación de correo
        electrónico / contraseña, `authenticate` devolverá` None`. Plantee una excepción
        en este caso.


        """
        if user is None:
            msg = 'Dirección de correo electronico y/o contraseña incorrecta.'
            raise exceptions.AuthenticationFailed(msg)

        """
        Django proporciona una bandera en nuestro modelo `Usuario` llamada` is_active`. los
        El propósito de esta bandera es decirnos si el usuario ha sido baneado.
        o desactivado. Este casi nunca será el caso, pero
        vale la pena comprobarlo. Plantee una excepción en este caso.


        """
        if not user.is_active:
            msg = 'Este usuario ha sido desactivado. Comuniquese con el administrador del sistema para mas información.'
            raise exceptions.AuthenticationFailed(msg)

        """
        Si la cuenta del usuario fue eliminada de manera temporal y si
        el usuario vuelve a iniciar sesión. Se activa la cuenta
        nuevamente.


        """
        if user.state == False:
            user.state = True

        """
        Django proporciona un metodo llamado save. Este metodo nos permite hacer una
        serie de transacciones antes de guardar un registro.
        Diríjase al modulo apps.users.models y busques el metodo save


        """
        user.save()

        """
        El método `validate` debería devolver un diccionario de datos validados.
        Estos son los datos que se pasan a los métodos `create` y` update`.


        """
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
