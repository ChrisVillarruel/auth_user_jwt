# users.models

import jwt
from django.db import models
from datetime import datetime, timedelta
import datetime
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    Django requiere que los usuarios personalizados definan su propia clase de administrador.
    La razon por la que se hereda de `BaseUserManager`, obtenemos gran parte del mismo código utilizado por
    Django para crear un `Usuario`.

    Todo lo que tenemos que hacer es anular la función `create_user` que usaremos
    para crear objetos "Usuario".
    """

    def create_user(self, username, email, password=None):
        """Crea y devuelve un "Usuario" con un correo electrónico, nombre de usuario y contraseña."""
        if username is None:
            raise TypeError('Los usuarios deben tener un nombre de usuario.')

        if email is None:
            raise TypeError('Los usuarios deben tener una dirección de correo electronico.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Crea y devuelve un 'usuario' como superusuario y permisos de (admin)
        """
        if password is None:
            raise TypeError('Los superusuarios deben tener una contraseña.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Identificador unico que se va incrementando de forma automatica
    user_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    # Cada "Usuario" necesita un identificador único legible por humanos que
    # podamos usar para representar el "Usuario" en la interfaz de usuario.
    # Queremos indexar esta columna en la base de datos para mejorar el rendimiento
    # de la búsqueda.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # También necesitamos una forma de contactar al usuario y una forma de que el usuario se identifiquen
    # ellos mismos al iniciar sesión. Dado que necesitamos una dirección de correo electrónico para contactar
    # el usuario de todos modos, también usaremos el correo electrónico para iniciar sesión porque es
    # la forma más común de credencial de inicio de sesión.
    email = models.EmailField(db_index=True, unique=True)

    # También necesitamos una forma de indetificar al usuario con su nombre
    first_name = models.CharField(db_index=True, max_length=255)

    # También necesitamos una forma de indetificar al usuario con su apellido
    last_name = models.CharField(db_index=True, max_length=255)

    # Cuando un usuario ya no desea utilizar nuestra plataforma, puede intentar eliminar
    # su cuenta. Eso es un problema para nosotros porque los datos que recopilamos son
    # valioso para nosotros y no queremos eliminarlo. Simplemente se le ofrecerá a los
    # usuarios una forma de desactivar su cuenta en lugar de
    # dejándolos borrarlo. De esa forma, ya no aparecerán en el sitio,
    # pero aún podemos analizar los datos.
    is_active = models.BooleanField(default=True)

    # Django espera que la bandera `is_staff` determina quien es admin y quien no
    # Para la mayoría de los usuarios, esta bandera siempre estará falso.
    is_staff = models.BooleanField(default=False)

    # Una marca de tiempo que representa cuándo se creó este objeto.
    created_at = models.DateTimeField(auto_now_add=True)

    # Una marca de tiempo que representa cuándo se actualizo este objeto.
    updated_at = models.DateTimeField(auto_now=True)

    # La propiedad `USERNAME_FIELD` nos dice qué campo usaremos para iniciar sesión.
    # En este caso, queremos que sea el campo de correo electrónico.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Le indicamos a Django que la clase UserManager definida anteriormente debería administrar
    # objetos de este tipo.
    objects = UserManager()

    def __str__(self):
        """
        Devuelve una representación en cadena de caracteres el correo
        de un usuario despues de haber creado el objeto.
        """
        return self.email

    @property
    def token(self):
        """
        Nos permite obtener el token de un usuario llamando a `user.token` en lugar de
        `usuario.generate_jwt_token ().

        El decorador `@ property` anterior lo hace posible. `token` se llama
        una "propiedad dinámica" y obtener el valor del atributo.
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        """
        Genera un token web JSON que almacena el ID de este usuario y tiene
        una caducidad fecha establecida en 60 días en el futuro.
        """
        return {
            'access_token': self.generate_jwt_access_token(),
            'refresh_token': self.generate_jwt_refresh_token()
        }

    def generate_jwt_access_token(self):
        """
        Generar un token de acceso JWT que almacena información del usuario que se registro y tiene
        un tiempo de vida muy reducida. Este tipo de token es utilizado para la activación
        de una cuenta. Su tiempo de vida va entre los cinco minutos y media hora.
        """

        access_token = jwt.encode({
            'id': self.user_id,
            'email': self.email,
            'username': self.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
        }, settings.SECRET_KEY, algorithm='HS256')

        return access_token.decode('utf-8')

    def generate_jwt_refresh_token(self):
        """
        Generar un refresh_token de JWT que almacena información del usuario que se registro y tiene
        un tiempo vida mas alrgo. Este tipo de token es utilizado para la navegación dentro del sistema
        sin la necesidad de iniciar sesión cada media hora. Este tipo de token puede durar el tiempo
        que el desarrollador decida. En este caso duarara 60 dias.
        """

        refresh_token = jwt.encode({
            'id': self.user_id,
            'email': self.email,
            'username': self.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60),
            'iat': datetime.datetime.utcnow()
        }, settings.SECRET_KEY, algorithm='HS256')

        return refresh_token.decode('utf-8')
