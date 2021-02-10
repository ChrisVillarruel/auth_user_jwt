# Django Rest Framwork - User Authenticate

### Descripción

Aplicación web Backent implementando la arquitectura REST. Esta aplicación mostrara el funcionamiento de la autenticación de usuarios y permisos de acceso de Django Rest Framwork. La autenticación esta basada en Tokens utilizando el estándar Json Web Token (JWT).

### Capturas

Para registrar un usuario, se accederá a la ruta, register.
Esta ruta accederá al controlador y el controlador enviara al serializador los datos de la petición actual. 

![This is a alt text.](/capturas/rutaRegister.png "This is a sample image.")

Ingresamos nuestros datos dentro de una estructura JSON y enviaremos nuestros datos para podernos registrar en la aplicación

![This is a alt text.](/capturas/jsonRegister.png "This is a sample image.")

Si el registro fue exitoso, me retornara la API mis datos ingresados y dos tokens.
Un Token de acceso y un Token de actualización.
El Token de acceso tiene un tipo de caducidad de media hora (30 min) y el Token de actualización tiene un tiempo de caducidad de 60 días.

![This is a alt text.](/capturas/registroExitoso.png "This is a sample image.")
