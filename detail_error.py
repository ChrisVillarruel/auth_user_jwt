from datetime import datetime


def base_resource(message, code):
    return {
        'detail': message,
        'status_code': code
    }


def resource_created():
    created = base_resource(message='Recurso Creado.', code=201)
    return created


def resource_updated():
    update = base_resource(message='Usuario Actualizado.', code=200)
    return update


def resource_destroy():
    destroy = base_resource(message='Cuenta Eliminada.', code=200)
    return destroy


def not_found():
    not_found = base_resource(message='No encontrado.', code=404)
    return not_found


def logout():
    logout = base_resource(message='Sesión Finalizada', code=204)
    return logout
