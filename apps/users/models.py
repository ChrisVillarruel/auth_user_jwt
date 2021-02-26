# Modulos de Django
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Modulos de python
from datetime import datetime, timedelta
import datetime
import pytz

# Modulos locales
from .generate_tokens import generate_jwt_access_token, generate_jwt_refresh_token
from .decode_token import get_token_expiration_date
from .abstract_models import UserToken, CreateOrUpdateUser


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


class User(AbstractBaseUser, PermissionsMixin, UserToken, CreateOrUpdateUser):
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

    def get_username(self):
        return f'{self.username}'

    def get_email(self):
        return self.email.lower()

    def token(self):
        """
        Nos permite obtener el token de un usuario llamando a `user.token` en lugar de
        `usuario.generate_jwt_token ().

        El decorador `@ property` anterior lo hace posible. `token` se llama
        una "propiedad dinámica" y obtener el valor del atributo.
        """

        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }

    def save(self, *args, **kwargs):
        date_now = datetime.datetime.now(tz=pytz.timezone('America/Mexico_City')).strftime('%y%m%d')

        # Si el campo refresh_token y access_token son vacios,
        # quiere decir que el usuario es nuevo, por lo tanto generamos
        # dos nuevos tokens
        if self.refresh_token is None or self.access_token is None:
            self.refresh_token = generate_jwt_refresh_token(self.email, self.username)
            self.access_token = generate_jwt_access_token(self.email, self.username)

        # Si al llamar al metodo save, la fecha actual a la que se llamo el
        # metodo es igual al dia anterior de la fecha de expiración del token,
        # creamos un nuevo token
        if date_now >= get_token_expiration_date(self.refresh_token):
            self.refresh_token = generate_jwt_refresh_token(self.email, self.username)

        super().save(*args, **kwargs)
