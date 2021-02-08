# users.serializers
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Solicita el registro de serializadores y crea un nuevo usuario. """

    email = serializers.EmailField(max_length=200, min_length=3)
    username = serializers.CharField(max_length=255, min_length=3)

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # El cliente no debería poder enviar un token junto con una solicitud de registro.
    # Hacemos el `token` de solo lectura para que maneje eso por nosotros.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    # Validaciones.
    # Validaremos que ningun dato entrate sea duplicado con un dato ya existente
    def validate_email(self, value):
        email = value
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('El correo electronico que usted ingreso ya existe.')

        return value.lower()

    def validate_username(self, value):
        username = value

        # Validamos que no existan caracteres especiales
        # Si llegan a existir me los mostrara atravez de una lista
        caracteres_prohibidos = []
        for u in username:
            if not u.isalnum():
                caracteres_prohibidos.append(u)

        if not username.isalnum():
            raise serializers.ValidationError(f'El nombre de usuario no debe de tener, {caracteres_prohibidos}')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('El nombre de usuario que usted ingreso ya existe.')

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # El método `validate` es donde nos aseguramos de que la
        # instancia de `LoginSerializer` tiene" válido ". En el caso de registrar un
        # usuario en, esto significa validar que ha proporcionado un correo electrónico
        # y contraseña y que esta combinación coincide con uno de los usuarios en
        # nuestra base de datos.
        email = data.get('email', None)
        password = data.get('password', None)

        # El método `authenticate` es proporcionado por Django y maneja la verificación
        # para un usuario que coincide con esta combinación de correo electrónico y contraseña. Date cuenta cómo
        # pasamos `email` como el valor de` username` ya que en nuestro User
        # modelo establecemos `USERNAME_FIELD` como` email`.
        user = authenticate(username=email, password=password)

        # Si no se encontró ningún usuario que coincida con esta combinación de correo electrónico / contraseña,
        # `authenticate` devolverá` None`. Plantee una excepción en este caso.
        if user is None:
            raise serializers.ValidationError(
                'No se encontró un usuario con este correo electrónico y contraseña.')

        # Django proporciona una bandera en nuestro modelo `Usuario` llamada` is_active`. los
        # El propósito de esta bandera es decirnos si el usuario ha sido baneado.
        # o desactivado. Este casi nunca será el caso, pero
        # vale la pena comprobarlo. Plantee una excepción en este caso.
        if not user.is_active:
            raise serializers.ValidationError(
                'Este usuario ha sido desactivado.')

        # El método `validate` debería devolver un diccionario de datos validados.
        # Estos son los datos que se pasan a los métodos `create` y` update`.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
