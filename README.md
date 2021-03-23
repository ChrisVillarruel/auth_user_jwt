# User Authenticate Web Token

### Descripción

Aplicación Web API escrito con Django-Rest-Framework aplicando el metodo de autenticación via tokens implementado el estandar Json-Web-Token (JWT). 

## Actualización.

Se añadio una nueva versión:

- Los tokens de autenticación ahora se almacenan en la base de datos.
- Un cierre de sesión mas robusto.
- Actualización de tokens automatizado.
- Menejo de errores mas robusto.

## Actualización | 10 de Marzo del 2021

Se añadio una nueva versión. Dentro de esta versión se añadieron grandes cambios dentro del codigo fuente.
Lo mas destacado de la actualización es:

- La Posibilidad de que un usuario pueda suspender su cuenta.
- La posibilidad de eliminar de forma definitiva la cuenta de un usuario.

Cambios dentro del codigo fuente:

- La implementación de vistas genericas.
- Implementación de modelos abstractos.
- Se mejoro la escalabilidad del codigo fuente.
- Se estructuro el sistema de archivos del proyecto.
- Se agrego un archivo de dependencias. 

## Actualización | 19 de marzon del 2021

Se añadio una nueva versión. Dentro de esta versión se añadieron cambios dentro del codigo fuente.
Lo mas destacado de la actualización es:

- Reducción de codigo repetido.
- Se implemento una nueva vista de cierre de sesión.
- Eliminación del seriaizador Logout.

## Actualización | 23 de marzo del 2021

Se detecto un error muy fuerte dentro de los permisos de acceso, por lo tanto, se crearon permisos personalizados con el 
objetivo de mejorar el acceso dentro de la aplicación sin embargo no es una solución definitiva pues se sigue investigando 
en cómo mejorar los permisos de acceso.

Lo mas destacado de la actualización es:

- Permisos personalizados.
  


#### Este repositorio sera actualizado constantemente.

## Ejemplo del funcionaminto del proyecto.

#### Regsitro de un Usuario

![This is a alt text.](/screenshots/user_register.png "This is a sample image.")

#### Registro Exitoso. 

![This is a alt text.](/screenshots/user_register_success.png "This is a sample image.")

#### Registro Fallido. 

![This is a alt text.](/screenshots/user_register_failure.png "This is a sample image.")
