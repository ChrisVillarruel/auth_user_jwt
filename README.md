# Django Rest Framwork - User Authenticate

### Descripción

Aplicación web Backent implementando la arquitectura REST. Esta aplicación mostrara el funcionamiento de la autenticación de usuarios y permisos de acceso de Django Rest Framwork. La autenticación esta basada en Tokens utilizando el estándar Json Web Token (JWT).

## Actualización.

Se creo una nueva versión de la aplicación.

- La posibilidad de almacenar los tokens de acceso y de actaulización en la base de datos.
- Un cierre de sesión mas seguro.
- Los tokens se actualizaran de manera automatica. Siempre y cuando el usuario ingrese sus crendenciales nuevamente.
- Control de errores mas robusto.

## Actualización | 10 de Marzo del 2021

Se actualizo la versión de la aplicación. En esta versión se realizaron grandes cambios dentro del codigo fuente.
Lo mas destacado de la actualización es:

- La posibilidad de que un usuario pueda suspender su cuenta.
- La posibilidad de eliminar de forma definitiva la cuenta de un usuario.

Cambios dentro del codigo fuente:

- La implementación de vistas genericas.
- Implementación de modelos abstractos.
- Se mejoro la escalabilidad del codigo fuente.
- Se estructuro el sistema de archivos del proyecto.
- Se agrego un archivo de dependencias. 


#### El repositorio se actualizara constantemente.

### Capturas

#### Regsitro de un Usuario
Para registrar un usuario, se accederá a la ruta, register.
Esta ruta accederá al controlador y el controlador enviara al serializador los datos de la petición actual. 

![This is a alt text.](/capturas/rutaRegister.png "This is a sample image.")

Ingresamos nuestros datos dentro de una estructura JSON y enviaremos nuestros datos para podernos registrar en la aplicación

![This is a alt text.](/capturas/jsonRegister.png "This is a sample image.")

Si el registro fue exitoso, me retornara la API mis datos ingresados y dos tokens.
Un Token de acceso y un Token de actualización.
El Token de acceso tiene un tiempo de caducidad de media hora (30 min) y el Token de actualización tiene un tiempo de caducidad de 60 días.

![This is a alt text.](/capturas/registroExitoso.png "This is a sample image.")

Decodificamos el Token y verificamos que los datos correspondan al usuario actual que se registro.

![This is a alt text.](/capturas/decodificacionToken.png "This is a sample image.")


#### Logeo de un usuario

Despues de que el usuario se haya registrado a continuación se va a logear en la aplicación.
El usuario se dirigira a la ruta login.

![This is a alt text.](/capturas/rutaLogin.png "This is a sample image.")

Se ingresara las credenciales correpondientes y la API realizara exacatemente lo mismo, se dirigira al controlador y el controlador le enviara al serializador 
su dirección de correo electroninco y contraseña. El serializador se encaragara de validar que el usuario exista y que se cuenta este actiavada. 
Si todo fue correcto la API retornara su email, nombre de usuario, los tokens de acceso y de actualización del sistema.

![This is a alt text.](/capturas/jsonLogin.png "This is a sample image.")

![This is a alt text.](/capturas/loginExitoso.png "This is a sample image.")

#### Verificamos que el usuario actual este logeado.

Para verificar que el usuario actual este logeado, nos dirigiremos a la ruta \user. Esta ruta retornara un JSON con todos los datos del usuario, email, nombre de usuario
y credenciales de acceso (Tokens).

![This is a alt text.](/capturas/detallaUsuario.png "This is a sample image.")

Si nosotros intentamos acceder a contenido sin estar autenticados y posteriormente autorizados por el sistema, me retornara el siguiente error de excepción.

![This is a alt text.](/capturas/accesoDenegado.png "This is a sample image.")

Para que el usuario actual pueda ver sus datos el frontent se encargara de enviarle al backent por medio de un token de autorización mismo que fue generado al iniciar sesión, que el usuario actual pertenece al sistema y que el token que el frontend envio fue firmado por el mismo sistema. De esta manera el sistema le dara permiso al usuario y retornara los datos del usuario. 

![This is a alt text.](/capturas/authorizationBearer.png "This is a sample image.")

![This is a alt text.](/capturas/authorizationExitosa.png "This is a sample image.")

#### Permisos de SuperUsuario

Si el usuario por pura coincidencia accede a secciones del sistema prohibidas la API esta preparada para denegar el acceso a usuarios no autorizados.

![This is a alt text.](/capturas/rutalistadoDeUsuarios.png "This is a sample image.")

El forntent realizara el mismo proceso, enviara un token de autorización del usuario actual. 

![This is a alt text.](/capturas/authorizationBearerListUser.png "This is a sample image.")

Sin embargo el sistema negara el acceso al recurso solicitado, en este caso el listado de los usuarios del sistema. Pues el recusro solicitado tiene información de cuentas de todos los usuarios.

![This is a alt text.](/capturas/permisoDenegado.png "This is a sample image.")

De lo contrario, si iniciamos sesión con un usuario que si cuente con permisos de administrador del sistema.

![This is a alt text.](/capturas/superUserLogin.png "This is a sample image.")

Y realizamos el proceso de autorización Bearer para acceder a los recursos del sistema. Me retornara un JSON con la información de todos los usuarios registrados en el sistema.

![This is a alt text.](/capturas/userslistSuperUser.png "This is a sample image.")






