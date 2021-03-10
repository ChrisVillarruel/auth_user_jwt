# Django Rest Framwork - User Authenticate

### Descripción

Aplicación web Backent implementando la arquitectura REST. Esta aplicación mostrara el funcionamiento de la autenticación de usuarios y permisos de acceso de Django Rest Framwork. La autenticación esta basada en Tokens utilizando el estándar Json Web Token (JWT).


## Actualización.

Se creo una nueva versión de la aplicación REST ubicada en la rama save_token. Los cambios mas notorios son:

- La posibilidad de almacenar los tokens de acceso y de actaulización en la base de datos.
- Un cierre de sesión mas seguro.
- Los tokens se actualizaran de manera automatica. Siempre y cuando el usuario ingrese sus crendenciales nuevamente.
- Control de errores mas robusto. 

