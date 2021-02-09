# users.serializers
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import exceptions

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
            raise exceptions.AuthenticationFailed(
                'Dirección de correo electronico y/o contraseña incorrecta')

        # Django proporciona una bandera en nuestro modelo `Usuario` llamada` is_active`. los
        # El propósito de esta bandera es decirnos si el usuario ha sido baneado.
        # o desactivado. Este casi nunca será el caso, pero
        # vale la pena comprobarlo. Plantee una excepción en este caso.
        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'Este usuario ha sido desactivado.')

        # El método `validate` debería devolver un diccionario de datos validados.
        # Estos son los datos que se pasan a los métodos `create` y` update`.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Las contraseñas deben tener al menos 8 caracteres, pero no más de 128
    # caracteres. Estos valores son los predeterminados proporcionados por Django. Podríamos
    # cambiarlos, pero eso crearía un trabajo extra sin introducir ningún
    # beneficio, así que sigamos con los valores predeterminados.
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

        # La opción `read_only_fields` es una alternativa para explícitamente
        # especificando el campo con `read_only = True` como hicimos para la contraseña
        # encima. La razón por la que queremos usar `read_only_fields` aquí es que
        # no necesitamos especificar nada más sobre el campo.
        # El campo de contraseña necesitaba el `min_length` y propiedades de `max_length`,
        # pero ese no es el caso del token campo.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Realiza una actualización en un usuario."""

        # Las contraseñas no deben manejarse con `setattr`, a diferencia de otros campos.
        # Django proporciona una función que maneja hash y
        # Salar contraseñas. Eso significa
        # necesitamos eliminar el campo de contraseña de la
        # Diccionario `validated_data` antes de iterar sobre él.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # Para las claves restantes en `validated_data`, las configuraremos en
            # la instancia actual de "Usuario" una a la vez.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password ()` maneja todo
            # de las cosas de seguridad que no deberían preocuparnos.
            instance.set_password(password)

        # Una vez actualizado todo, debemos guardar explícitamente
        # el modelo. Vale la pena señalar que `.set_password ()` no
        # guarda el modelo.
        instance.save()

        return instance
