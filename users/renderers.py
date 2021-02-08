import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # Si recibimos una clave "token" como parte de la respuesta, será una
        # objeto de byte. Los objetos de bytes no se serializan bien, por lo que necesitamos
        # decodificarlo antes de renderizar el objeto Usuario.
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            # También como se mencionó anteriormente, decodificaremos `token` si es de tipo
            # bytes.
            data['token'] = token.decode('utf-8')
            print(data['token'])
        # Finalmente, podemos representar sus datos en el espacio de nombre de "usuario".
        return json.dumps({
            'user': data
        })
