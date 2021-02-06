# users.serializers
from rest_framework import serializers

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
