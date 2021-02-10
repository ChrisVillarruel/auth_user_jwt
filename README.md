# Django Rest Framwork - User Authenticate

### Descripción

Aplicación web Backent implementando la arquitectura REST. Esta aplicación mostrara el funcionamiento de la autenticación de usuarios y permisos de acceso de Django Rest Framwork. La autenticación esta basada en Tokens utilizando el estándar Json Web Token (JWT).

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
Si todo fue correcto la api retornara su email, nombre de usuario y los tokens de acceso y de actualización del sistema.

![This is a alt text.](/capturas/jsonLogin.png "This is a sample image.")

![This is a alt text.](/capturas/loginExitoso.png "This is a sample image.")












