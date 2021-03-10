
# Modulos de rest_framework
from rest_framework import serializers

# Modulo local
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

        """
        La opción `read_only_fields` es una alternativa para explícitamente
        especificando el campo con `read_only = True` como hicimos para la contraseña
        encima. La razón por la que queremos usar `read_only_fields` aquí es que
        no necesitamos especificar nada más sobre el campo.
        El campo de contraseña necesitaba el `min_length` y propiedades de `max_length`,
        pero ese no es el caso del token campo.


        """
        read_only_fields = ('token',)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if user.state == False:
            msg = 'La cuenta de este usuario fue dada de baja temporal.'
            raise serializers.ValidationError(msg)

        return value

    def update(self, instance, validated_data):
        """
        Realiza una actualización en un usuario.

        Las contraseñas no deben manejarse con `setattr`, a diferencia de otros campos.
        Django proporciona una función que maneja hash y
        permite saltar contraseñas. Eso significa que
        necesitaremos eliminar el campo de contraseña de
        Diccionario `validated_data` antes de iterar sobre él.


        """
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            """
            Para las claves restantes en `validated_data`, las configuraremos en
            la instancia actual de "Usuario" una a la vez.


            """
            setattr(instance, key, value)

        if password is not None:
            """
            `.set_password ()` es el que se encarga de poner la encriptación del
            password.


            """
            instance.set_password(password)

        """
        Una vez actualizado todo, debemos guardar explícitamente
        el modelo. Vale la pena señalar que `.set_password ()` no
        guarda el modelo.


        """
        instance.save()

        return instance
