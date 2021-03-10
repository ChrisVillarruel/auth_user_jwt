# modulos nativos de rest_framework
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Modulos locales
from apps.users.models import User
from detail_error import msg_error
# from users.renderers import UserJSONRenderer
from apps.users.api.serializers.login_serializer import LoginSerializer
from apps.users.api.serializers.user_serializer import UserSerializer
from apps.users.api.serializers.logout_serializer import LogoutSerializer
from apps.users.api.serializers.register_serializer import RegistrationSerializer
from apps.users.api.serializers.admin_serializer import UserListSerializer, UserDetailSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Si el registro sale correcto retornara un objeto con los datos
    del usuario y si hay un error, retornara un objeto de tipo error.


    """
    serializer_class = RegistrationSerializer
    permissions_classes = (AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error = msg_error('Error de validación', 'BAD_REQUEST', 400, serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Si el logeo es correcto retornara un objeto con los datos del
    usuario y si hay un error, retornara un objeto de tipo error.


    """
    permissions_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        error = msg_error('Error de validación', 'BAD_REQUEST', 400, serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    Para que el usuario pueda cerrar sesión, el cliente debera enviar
    el token de actualización para que el servidor cancele el token y
    genere uno nuevo.


    """
    permissions_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response({'message': 'Sesión Finalizada. Vuelva pronto!'}, status=status.HTTP_204_NO_CONTENT)

        error = msg_error('Error de validación', 'BAD_REQUEST', 400, serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permissions_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self, email):
        if email is not None:
            return self.get_serializer().Meta.model.objects.filter(email=email).first()

    def retrieve(self, request, *args, **kwargs):
        """
        No hay nada que validar o guardar aquí. En su lugar,
        solo queremos que el serializadornse se encargue de convertir
        nuestro objeto `User` en algo que pueda ser JSON y enviarlo al cliente.

        Esta vista solo mostrara la información del usuario


        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Se actualizara de manera parcial los datos del usuario


        """
        serializer = self.serializer_class(self.get_queryset(request.user), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Tus datos se actualizaron con exito.'}, status=status.HTTP_200_OK)

    def destroy(self, request):
        user = self.get_queryset(request.user)

        if user is not None:
            user.state = False
            user.save()

            msg = {'message': 'Su cuenta se dio de baja. Regresa cuando gustes!'}
            return Response(msg, status=status.HTTP_200_OK)

        error = msg_error('Error', 'BAD_REQUEST', 400, 'Ups. Ocurrio un error en su sesión actual.')
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
