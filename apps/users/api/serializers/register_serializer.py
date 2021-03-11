
# Modulos de rest_framework
from rest_framework import serializers

# Modulos locales
from apps.users.models import User


def get_special_characters(username):
    list_characters = []

    for special_characters in username:
        if not special_characters.isalnum():
            list_characters.append(special_characters)

    return list_characters


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Los datos enviados por el cliente se serializara a un diccionario
    de python nativo y retornara un JSON

    """

    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

        """
        El cliente no debería poder enviar un token junto con una solicitud de registro.
        Hacemos el `token` de solo lectura para que maneje eso por nosotros.


        """
        read_only_fields = ('token',)

    def validate_email(self, value):
        """
        Validaciones.
        Validaremos que ningun dato entrate sea duplicado con un dato ya existente


        """

        if User.objects.filter(email=value).exists():
            msg = 'La direccióm de correo electronico que usted ingreso ya existe.'
            raise serializers.ValidationError(msg)

        return value.lower()

    def validate_username(self, value):
        """
        Validamos que no existan caracteres especiales
        Si llegan a existir los mostrara dentro de una lista.

        Validamos que el nombre de usuario no este duplicado.


        """
        special_characters = get_special_characters(value)

        if User.objects.filter(username=value).exists():
            msg = 'El nombre de usuario que usted ingreso ya existe.'
            raise serializers.ValidationError(msg)

        if value.isnumeric():
            msg = 'Nombre de usuario no valido. Asegurese que el nombre de usuario sea alfanumerico'
            raise serializers.ValidationError(msg)

        if not value.isalnum():
            msg = f'Caracteres no validos {special_characters}.'
            raise serializers.ValidationError(msg)

        return value

    def create(self, validated_data):
        """
        Despues de el diccionario haya sido validado
        con '**validated_data' tomaremos solo los valores
        del diccionario para así crear un usuario


        """
        return User.objects.create_user(**validated_data)
